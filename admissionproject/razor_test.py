import razorpay
client = razorpay.Client(auth=("rzp_test_dummykey123", "dummysecretdummy"))
try:
    client.order.create({
        "amount": 50000,
        "currency": "INR",
        "payment_capture": "1"
    })
except Exception as e:
    print(repr(e))
