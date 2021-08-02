from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment


class PayPalClient:
    def __init__(self):
        self.client_id = "AT5Mh30nKl4JBoKkFr_LWk6aSkua95cEh3y0uxh2nJKp3VQzOezROjDNyY0PaHwzhmDoafM-40Futktd"
        self.client_secret = "EEbEkQKn3jaT3o1aPHjR0SEXLkCQy6MEoIYQHyzxEDWYHucAA3Mwn6dx_TfLNY3uDG6KGViP1RZz4nZH"
        self.environment = SandboxEnvironment(client_id=self.client_id, client_secret=self.client_secret)
        self.client = PayPalHttpClient(self.environment)