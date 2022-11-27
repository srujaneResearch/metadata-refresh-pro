import stripe

stripe.api_key = "sk_test_51M2rqGITV27aYUdhCpJp3IUmIHF9RgbZUUVHdbanHPA85wgiaYMjWg8OJbaGYuwpehdAzJ0DjJ3vLEMy98a4nFZl00V7kFy5x4"

l = stripe.PaymentLink.create(
    line_items=[{'price':'price_1M7LROITV27aYUdhO9icaCAR','quantity':'1'}],
    metadata = {'chat_id':'srujan bhai'}
)

customer = 'cus_MsC3f4vKViOG0u'

m = stripe.billing_portal.Session.create(customer=customer)