import mailbox

mailing_lists = ["kewgardens"]


# Detect if a message is spam or not
def is_spam(msg: mailbox.MaildirMessage) -> bool:
    return False


# Process an individual message
# extract subject, author, just text (no mime attachments/html)
def process(msg: mailbox.MaildirMessage):
    sender = msg["From"]
    date = msg["Date"]
    subject = msg["Subject"]
    contents = ""
    for part in msg.walk():
        if part.get_content_type() == "text/plain" or part.get_content_type() == "text/html":
            contents += part.get_payload(decode = True).decode('utf-8')
    print(sender)
    print(date)
    print(subject)
    print(contents)
    #for k, v in msg.items():
    #    print("Key: ", k, "Value: ", v)


# Find all the text from each message and store it
# along with the subject and author in Mongo
# potentially check if went through spam filter first
# and also eliminate messages by non-registered users
# Delete messages when done with them
def store_and_delete(mailing_list: str):
    md = mailbox.Maildir('/home/ubuntu/' + mailing_list + '/Maildir')
    for msg in md:
        # only look at new messages
        if msg.get_subdir() == "new":
            process(msg)
    return


if __name__ == "__main__":
    for mailing_list in mailing_lists:
        store_and_delete(mailing_list)
