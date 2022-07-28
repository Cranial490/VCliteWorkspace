# VCliteWorkspace
VClite is a peer to peer trading platform meant mainly for pre-IPO shares.<br><br>
![order flow](https://user-images.githubusercontent.com/23013907/181655440-e776dd34-7068-4c2c-b8cc-06d4af77e2e6.jpg)
<br>
Current version of VClite has
- Login/Registration with OTP verification
- Efficient order matching 
- Notifying users of matched orders
- Generating receipt for both parties

Backend : Django, postgres, AWS RDS, AWS EC2 <br>
Frontend: VueJS, AWS Amplify

```
To get started
- clone repo
- pipenv install (To install dependencies from pipfile)
- pipenv shell (start virtual environment)
- python manage.py runserver 
- To startup front-end 'cd' to vc-app
- npm install (To install dependencies from package.json)
- npm run dev
```
