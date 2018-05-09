import mailbox
import settings
import datetime
from item import Item
from database_manager import DatabaseManager
from email.utils import parseaddr


# Detect if a message is spam or not
def is_spam(msg: mailbox.MaildirMessage) -> bool:
    return False


# Process an individual message
# extract subject, author, just text (no mime attachments)
def process(msg: mailbox.MaildirMessage) -> Item:
    sender, address = parseaddr(msg["From"])
    date = datetime.datetime.utcfromtimestamp(msg.get_date()).isoformat() # ISO 8601 format
    subject = msg["Subject"]
    content = ""
    for part in msg.walk():
        if part.get_content_type() == "text/plain" or part.get_content_type() == "text/html":
            content += part.get_payload(decode = True).decode('utf-8')
    print(sender)
    print(address)
    print(date)
    print(subject)
    print(content)
    return Item(sender, address, date, subject, content)
    #for k, v in msg.items():
    #    print("Key: ", k, "Value: ", v)


# Find all the text from each message and store it
# along with the subject and author in Mongo
# potentially check if went through spam filter first
# and also eliminate messages by non-registered users
# Delete messages when done with them
def store_and_delete(mailing_list: str):
    with DatabaseManager(mailing_list) as db:
        md = mailbox.Maildir(settings.STEPOUT_BASE_PATH + mailing_list + '/Maildir')
        for key, msg in md.iteritems():
            # only look at new messages
            if msg.get_subdir() == "new":
                item = process(msg)
                db.store_item(item)
                md.remove(key)
                msg.set_subdir("cur")
                md.add(msg)


if __name__ == "__main__":
    for mailing_list in settings.MAILING_LISTS:
        store_and_delete(mailing_list)
