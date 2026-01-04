# cloud/hybrid.py
# 2Aether Hybrid Cloud — The $25B+ Button
# @realdavejags — Nov 28 2025

import os
import json
import boto3
from pathlib import Path
from datetime import datetime
from botocore.exceptions import NoCredentialsError, ClientError

# Global toggle — default = cloudless
HYBRID_MODE = False
S3_BUCKET = "2aether-hybrid-backup"  # Create this bucket in AWS


def enable_hybrid(mode: bool = True):
	global HYBRID_MODE
	HYBRID_MODE = mode
	status = "ENABLED" if mode else "DISABLED"
	print(f"2AETHER HYBRID CLOUD {status} — $25B+ BUTTON FLIPPED")
	return {"hybrid_mode": HYBRID_MODE, "status": status}


def upload_to_hybrid(file_path: str):
	if not HYBRID_MODE:
		return {"status": "cloudless — local only"}

	path = Path(file_path)
	if not path.exists():
		return {"error": "File not found"}

	s3 = boto3.client('s3')

	try:
		s3.upload_file(
			str(path),
			S3_BUCKET,
			path.name,
			ExtraArgs={"ACL": "private", "ContentType": "text/html"}
		)
		url = s3.generate_presigned_url(
			'get_object',
			Params={'Bucket': S3_BUCKET, 'Key': path.name},
			ExpiresIn=604800  # 7 days
		)
		print(f"HYBRID UPLOAD SUCCESS — {path.name}")
		return {"status": "uploaded", "url": url, "file": path.name}
	except NoCredentialsError:
		return {"error": "AWS credentials missing"}
	except ClientError as e:
		return {"error": str(e)}


def download_from_hybrid(filename: str):
	if not HYBRID_MODE:
		return {"status": "cloudless — local only"}

	s3 = boto3.client('s3')

	try:
		local_path = Path("recordings") / filename
		s3.download_file(S3_BUCKET, filename, str(local_path))
		print(f"HYBRID DOWNLOAD SUCCESS — {filename}")
		return {"status": "downloaded", "path": str(local_path)}
	except NoCredentialsError:
		return {"error": "AWS credentials missing"}
	except ClientError as e:
		return {"error": str(e)}


def auto_sync_latest():
	if not HYBRID_MODE:
		return {"status": "cloudless mode — no sync"}

	recordings = Path("recordings")
	latest_html = max(recordings.glob("*.2aether.html"), key=os.path.getctime, default=None)
	latest_report = max(recordings.glob("*.ai_report.json"), key=os.path.getctime, default=None)

	results = []
	if latest_html:
		results.append(upload_to_hybrid(latest_html))
	if latest_report:
		results.append(upload_to_hybrid(latest_report))

	return {"auto_sync": results, "timestamp": datetime.now().isoformat()}


if __name__ == "__main__":
	enable_hybrid(True)  # Flip the $25B button
	result = auto_sync_latest()
	print(json.dumps(result, indent=2))
	print("DAY 7 COMPLETE — HYBRID CLOUD LIVE — $25B+ VALUATION UNLOCKED")