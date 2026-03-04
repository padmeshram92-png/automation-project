def check_trigger(trigger):

    if trigger == "manual_trigger":
        return True

    elif trigger == "new_email":
        print("Checking for new email...")
        return True

    elif trigger == "new_order":
        print("Checking for new order...")
        return True

    elif trigger == "webhook":
        print("Webhook trigger received")
        return True

    else:
        return False
