from storages.backends.s3boto import S3BotoStorage

MediaRootS3BotoStorage  = lambda: S3BotoStorage(location='assets')