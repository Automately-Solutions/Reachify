import requests

def send_simple_message():
	return requests.post(
		"https://api.mailgun.net/v3/sandbox6008c1aa5b2b4e3d85454637f6c5cd1a.mailgun.org/messages",
		auth=("api", "91891beef826163c25871e4b8be19af2-4c205c86-6830b78f"),
		data={"from": "Mailgun Sandbox <postmaster@sandbox6008c1aa5b2b4e3d85454637f6c5cd1a.mailgun.org>",
			"to": "Pixelevate Solutions <pixelevatessolutions@gmail.com>",
			"subject": "Hello Pixelevate Solutions",
			"text": "Congratulations Pixelevate Solutions, you just sent an email with Mailgun! You are truly awesome!"})

send_simple_message()