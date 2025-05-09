import africastalking

def initialize_sms_service(username, api_key):
    africastalking.initialize(username, api_key)
    return africastalking.SMS

def send_sms_notification(phone_number, message):
    sms = initialize_sms_service(
        current_app.config['AFRICAS_TALKING_USERNAME'],
        current_app.config['AFRICAS_TALKING_API_KEY']
    )
    
    try:
        response = sms.send(message, [phone_number], current_app.config['AFRICAS_TALKING_SENDER_ID'])
        return response
    except Exception as e:
        current_app.logger.error(f"SMS sending failed: {str(e)}")
        raise