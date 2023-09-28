class AwsAccount:
    
    def __init__(self, aws_account, aws_service):
        self.account = aws_account
        self.service = aws_service
        self.contents = None