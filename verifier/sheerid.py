"""SheerID student verification API client"""
import re
import random
from typing import Dict, Optional

import httpx

from . import config
from .identity import NameGenerator, generate_psu_email, generate_birth_date, generate_psu_id
from .document import generate_image


class SheerIDVerifier:
    """SheerID student identity verifier implementing 6-step API flow"""

    def __init__(self, verification_id: str):
        self.verification_id = verification_id
        self.device_fingerprint = self._generate_device_fingerprint()

    @staticmethod
    def _generate_device_fingerprint() -> str:
        """Generate random 32-character hex device fingerprint"""
        charset = "0123456789abcdef"
        return ''.join(random.choice(charset) for _ in range(32))

    @staticmethod
    def parse_verification_id(url: str) -> Optional[str]:
        """Extract verificationId from SheerID URL using regex"""
        match = re.search(r"verificationId=([a-f0-9]+)", url, re.IGNORECASE)
        return match.group(1) if match else None

    def verify(self) -> Dict:
        """Execute 6-step SheerID verification flow
        
        Returns:
            Dict with keys: success, pending, message, verification_id, redirect_url
        """
        http_client = httpx.Client(timeout=30.0)
        
        try:
            name = NameGenerator().generate()
            first_name = name['first_name']
            last_name = name['last_name']
            email = generate_psu_email(first_name, last_name)
            birth_date = generate_birth_date()
            psu_id = generate_psu_id()
            school_id = config.DEFAULT_SCHOOL_ID
            school = config.SCHOOLS[school_id]
            
            img_data = generate_image(first_name, last_name, psu_id)
            file_size = len(img_data)
            
            step2_body = {
                "firstName": first_name,
                "lastName": last_name,
                "birthDate": birth_date,
                "email": email,
                "organization": {
                    "id": int(school_id),
                
                },
                "deviceFingerprintHash": self.device_fingerprint,
                "locale": "en-US",
                "metadata": {
                    "flags": '{"codeApplied":false}',
                    "submissionOptIn": "I agree to SheerID's Terms of Use and Privacy Policy, and to the business' collection and use of my personal information as described in its privacy policy.",
                    "refererUrl": f"{config.SHEERID_BASE_URL}/verify/{config.PROGRAM_ID}/?verificationId={self.verification_id}"
                }
            }
            
            step2_resp = http_client.post(
                f"{config.SHEERID_BASE_URL}/rest/v2/verification/{self.verification_id}/step/collectStudentPersonalInfo",
                json=step2_body,
                headers={"Content-Type": "application/json"}
            )
            
            if step2_resp.status_code != 200:
                return {
                    "success": False,
                    "pending": False,
                    "message": f"Step 2 failed (status {step2_resp.status_code}): {step2_resp.text}",
                    "verification_id": self.verification_id,
                    "redirect_url": None
                }
            
            step2_data = step2_resp.json()
            current_step = step2_data.get("currentStep")
            
            if current_step == "sso":
                http_client.delete(
                    f"{config.SHEERID_BASE_URL}/rest/v2/verification/{self.verification_id}/step/sso"
                )
            
            step4_body = {
                "files": [{
                    "fileName": "student_card.png",
                    "mimeType": "image/png",
                    "fileSize": file_size
                }]
            }
            
            step4_resp = http_client.post(
                f"{config.SHEERID_BASE_URL}/rest/v2/verification/{self.verification_id}/step/docUpload",
                json=step4_body,
                headers={"Content-Type": "application/json"}
            )
            
            if step4_resp.status_code != 200:
                return {
                    "success": False,
                    "pending": False,
                    "message": f"Step 4 failed (status {step4_resp.status_code}): {step4_resp.text}",
                    "verification_id": self.verification_id,
                    "redirect_url": None
                }
            
            step4_data = step4_resp.json()
            upload_url = step4_data.get("documents", [{}])[0].get("uploadUrl")
            
            if not upload_url:
                return {
                    "success": False,
                    "pending": False,
                    "message": "Failed to get S3 upload URL",
                    "verification_id": self.verification_id,
                    "redirect_url": None
                }
            
            s3_resp = http_client.put(
                upload_url,
                content=img_data,
                headers={"Content-Type": "image/png"},
                timeout=60.0
            )
            
            if not (200 <= s3_resp.status_code < 300):
                return {
                    "success": False,
                    "pending": False,
                    "message": f"S3 upload failed (status {s3_resp.status_code})",
                    "verification_id": self.verification_id,
                    "redirect_url": None
                }
            
            step6_resp = http_client.post(
                f"{config.SHEERID_BASE_URL}/rest/v2/verification/{self.verification_id}/step/completeDocUpload",
                headers={"Content-Type": "application/json"}
            )
            
            if step6_resp.status_code != 200:
                return {
                    "success": False,
                    "pending": False,
                    "message": f"Step 6 failed (status {step6_resp.status_code}): {step6_resp.text}",
                    "verification_id": self.verification_id,
                    "redirect_url": None
                }
            
            step6_data = step6_resp.json()
            
            return {
                "success": True,
                "pending": True,
                "message": "Document submitted, pending review",
                "verification_id": self.verification_id,
                "redirect_url": step6_data.get("redirectUrl")
            }
            
        except Exception as e:
            return {
                "success": False,
                "pending": False,
                "message": str(e),
                "verification_id": self.verification_id,
                "redirect_url": None
            }
        finally:
            http_client.close()
