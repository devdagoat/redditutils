import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import quote

_UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
_SEC_CH_UA = '"Not?A_Brand";v="99", "Opera";v="97", "Chromium";v="111"'

_DEFAULT_USER = "eyJwcmVmcyI6eyJ0b3BDb250ZW50RGlzbWlzc2FsVGltZSI6MCwiZ2xvYmFsVGhlbWUiOiJSRURESVQiLCJuaWdodG1vZGUiOnRydWUsImNvbGxhcHNlZFRyYXlTZWN0aW9ucyI6eyJmYXZvcml0ZXMiOmZhbHNlLCJtdWx0aXMiOmZhbHNlLCJtb2RlcmF0aW5nIjpmYWxzZSwic3Vic2NyaXB0aW9ucyI6ZmFsc2UsInByb2ZpbGVzIjpmYWxzZX0sInRvcENvbnRlbnRUaW1lc0Rpc21pc3NlZCI6MH19"
_DATADOME_PAYLOAD = "jsData=%7B%22ttst%22%3A58.40000003576279%2C%22ifov%22%3Afalse%2C%22tagpu%22%3A7.409355641195251%2C%22glvd%22%3A%22Google%20Inc.%20(NVIDIA)%22%2C%22glrd%22%3A%22ANGLE%20(NVIDIA%2C%20NVIDIA%20GeForce%20RTX%203060%20Laptop%20GPU%20Direct3D11%20vs_5_0%20ps_5_0%2C%20D3D11)%22%2C%22hc%22%3A16%2C%22br_oh%22%3A1032%2C%22br_ow%22%3A1920%2C%22ua%22%3A%22Mozilla%2F5.0%20(Windows%20NT%2010.0%3B%20Win64%3B%20x64)%20AppleWebKit%2F537.36%20(KHTML%2C%20like%20Gecko)%20Chrome%2F111.0.0.0%20Safari%2F537.36%20OPR%2F97.0.0.0%22%2C%22wbd%22%3Afalse%2C%22wdif%22%3Afalse%2C%22wdifrm%22%3Afalse%2C%22npmtm%22%3Afalse%2C%22br_h%22%3A923%2C%22br_w%22%3A1880%2C%22nddc%22%3A0%2C%22rs_h%22%3A1080%2C%22rs_w%22%3A1920%2C%22rs_cd%22%3A24%2C%22phe%22%3Afalse%2C%22nm%22%3Afalse%2C%22jsf%22%3Afalse%2C%22lg%22%3A%22en-US%22%2C%22pr%22%3A1%2C%22ars_h%22%3A1032%2C%22ars_w%22%3A1920%2C%22tz%22%3A-180%2C%22str_ss%22%3Atrue%2C%22str_ls%22%3Atrue%2C%22str_idb%22%3Atrue%2C%22str_odb%22%3Atrue%2C%22plgod%22%3Afalse%2C%22plg%22%3A5%2C%22plgne%22%3Atrue%2C%22plgre%22%3Atrue%2C%22plgof%22%3Afalse%2C%22plggt%22%3Afalse%2C%22pltod%22%3Afalse%2C%22hcovdr%22%3Afalse%2C%22hcovdr2%22%3Afalse%2C%22plovdr%22%3Afalse%2C%22plovdr2%22%3Afalse%2C%22ftsovdr%22%3Afalse%2C%22ftsovdr2%22%3Afalse%2C%22lb%22%3Afalse%2C%22eva%22%3A33%2C%22lo%22%3Afalse%2C%22ts_mtp%22%3A0%2C%22ts_tec%22%3Afalse%2C%22ts_tsa%22%3Afalse%2C%22vnd%22%3A%22Google%20Inc.%22%2C%22bid%22%3A%22NA%22%2C%22mmt%22%3A%22application%2Fpdf%2Ctext%2Fpdf%22%2C%22plu%22%3A%22PDF%20Viewer%2CChrome%20PDF%20Viewer%2CChromium%20PDF%20Viewer%2CMicrosoft%20Edge%20PDF%20Viewer%2CWebKit%20built-in%20PDF%22%2C%22hdn%22%3Afalse%2C%22awe%22%3Afalse%2C%22geb%22%3Afalse%2C%22dat%22%3Afalse%2C%22med%22%3A%22defined%22%2C%22aco%22%3A%22probably%22%2C%22acots%22%3Afalse%2C%22acmp%22%3A%22probably%22%2C%22acmpts%22%3Atrue%2C%22acw%22%3A%22probably%22%2C%22acwts%22%3Afalse%2C%22acma%22%3A%22maybe%22%2C%22acmats%22%3Afalse%2C%22acaa%22%3A%22probably%22%2C%22acaats%22%3Atrue%2C%22ac3%22%3A%22%22%2C%22ac3ts%22%3Afalse%2C%22acf%22%3A%22probably%22%2C%22acfts%22%3Afalse%2C%22acmp4%22%3A%22maybe%22%2C%22acmp4ts%22%3Afalse%2C%22acmp3%22%3A%22probably%22%2C%22acmp3ts%22%3Afalse%2C%22acwm%22%3A%22maybe%22%2C%22acwmts%22%3Afalse%2C%22ocpt%22%3Afalse%2C%22vco%22%3A%22probably%22%2C%22vcots%22%3Afalse%2C%22vch%22%3A%22probably%22%2C%22vchts%22%3Atrue%2C%22vcw%22%3A%22probably%22%2C%22vcwts%22%3Atrue%2C%22vc3%22%3A%22maybe%22%2C%22vc3ts%22%3Afalse%2C%22vcmp%22%3A%22%22%2C%22vcmpts%22%3Afalse%2C%22vcq%22%3A%22%22%2C%22vcqts%22%3Afalse%2C%22vc1%22%3A%22probably%22%2C%22vc1ts%22%3Atrue%2C%22dvm%22%3A8%2C%22sqt%22%3Afalse%2C%22so%22%3A%22landscape-primary%22%2C%22wdw%22%3Atrue%2C%22cokys%22%3A%22bG9hZFRpbWVzY3Npc2VhcmNoYXBwL%3D%22%2C%22ecpc%22%3Afalse%2C%22lgs%22%3Atrue%2C%22lgsod%22%3Afalse%2C%22psn%22%3Atrue%2C%22edp%22%3Atrue%2C%22addt%22%3Atrue%2C%22wsdc%22%3Atrue%2C%22ccsr%22%3Atrue%2C%22nuad%22%3Atrue%2C%22bcda%22%3Afalse%2C%22idn%22%3Atrue%2C%22capi%22%3Afalse%2C%22svde%22%3Afalse%2C%22vpbq%22%3Atrue%2C%22ucdv%22%3Afalse%2C%22spwn%22%3Afalse%2C%22emt%22%3Afalse%2C%22bfr%22%3Afalse%2C%22dbov%22%3Afalse%2C%22cfpfe%22%3A%22ZnVuY3Rpb24obyx0KXtmb3IodmFyIGE9ImNodW5rQ1NTLyIrKHtPbmJvYXJkaW5nTW9kYWw6Ik9uYm9hcmRpbmdNb2RhbCIsInJlZGRpdC1jb21wb25lbnRzLVFyQ29kZU1vZGFsIjoicmVkZGl0LWNvbXBvbmVudHMtUXJDb2RlTW9kYWwiLEFjaGlldmVtZW50c0Fj%22%2C%22stcfp%22%3A%22anM6MToxNTA4OTIKICAgIGF0IG5ldyBQcm9taXNlICg8YW5vbnltb3VzPikKICAgIGF0ICQgKGh0dHBzOi8vd3d3LnJlZGRpdHN0YXRpYy5jb20vZGVza3RvcDJ4L0NoYXR%2BR292ZXJuYW5jZX5SZWRkaXQuNGRhMTZkMDQ5MTU2MzJjNDMzODIuanM6MToxNTA4NDcp%22%2C%22prm%22%3Atrue%2C%22tzp%22%3A%22Europe%2FIstanbul%22%2C%22cvs%22%3Atrue%2C%22usb%22%3A%22defined%22%2C%22jset%22%3A1681502483%2C%22dcok%22%3A%22.reddit.com%22%2C%22mp_cx%22%3A347%2C%22mp_cy%22%3A139%2C%22mp_tr%22%3Atrue%2C%22mp_mx%22%3A-8%2C%22mp_my%22%3A3%2C%22mp_sx%22%3A387%2C%22mp_sy%22%3A248%2C%22mm_md%22%3A34%2C%22es_sigmdn%22%3A0.00045205266301718167%2C%22es_mumdn%22%3A8.484218662164482%2C%22es_distmdn%22%3A398.9636574927596%2C%22es_angsmdn%22%3A0.9272952180016123%2C%22es_angemdn%22%3A0.009174054545111285%7D&eventCounters=%7B%22mousemove%22%3A23%2C%22click%22%3A0%2C%22scroll%22%3A0%2C%22touchstart%22%3A0%2C%22touchend%22%3A0%2C%22touchmove%22%3A0%2C%22keydown%22%3A0%2C%22keyup%22%3A0%7D&jsType=le&cid=6ZBlpdoHN7slAtR_mohnHPjcy9LywLd-cXCXmvtHUp-2cS-52cCz9j6NyhLmP_5zOa1vQaNkda4UMlmq73zHI27x3wwm0DYHTiGa-BE5TKmnrfrHp61GXfYWE4lYgR9v&ddk=288922D4BE1987530B4E5D4A17952C&Referer=https%253A%252F%252Fwww.reddit.com%252F&request=%252F&responsePage=origin&ddv=4.7.2"
# ^^ these 2 will be passed as cookies, decreasing detection rate

_LOCALHOST = "http://localhost:8080"

_CLIENT_ID_REGX = re.compile('developed-app-(.*)\\" class=\\"developed-app')
_CLIENT_SECRET_REGX = re.compile('"prefright\\"&gt;(.*)&lt;\/td&gt;&lt;\/tr&gt;&lt;tr&gt;&lt;th&gt;name') #type: ignore

class LoginUtils:

    def __init__(self,username:str,password:str) -> None:
        self.username = username
        self.password = password
        self.session = requests.Session()
        self.session.headers.update({"User-Agent":_UA,"Sec-Ch-Ua":_SEC_CH_UA})
        self.session.head("https://www.reddit.com")
        self.session.cookies.update({"USER":_DEFAULT_USER,"datadome":self.get_datadome()})
        csrf_token = self.get_csrf()
        self.login(csrf_token) #type: ignore


    def get_datadome(self,payload:str=_DATADOME_PAYLOAD) -> str: #type: ignore
        headers = {
            "User-Agent":_UA,
            "Sec-Ch-Ua":_SEC_CH_UA,
            "Content-Type":"application/x-www-form-urlencoded"
        }
        resp = requests.post("https://api-js.datadome.co/js/",data=payload,headers=headers).json()
        if resp["status"] == 200:
            return resp["cookie"].split(";")[0][9:] 

    def get_csrf(self) -> str:
        resp = self.session.get("https://www.reddit.com/login/")
        soup = BeautifulSoup(resp.content,'html.parser')
        return soup.find("input",{"name":"csrf_token"})["value"] #type: ignore

    def login(self,csrf:str) -> None:
        payl = f"csrf_token={csrf}&otp=&password={quote(self.password)}&dest=https%3A%2F%2Fwww.reddit.com&username={self.username}"
        self.session.post("https://www.reddit.com/login",data=payl)

    def get_auth_bearer(self) -> str:
        resp = self.session.get("https://www.reddit.com/appeal")
        return re.search('"accessToken":"(.*)","expires":',resp.text).group(1) #type: ignore

    def appeal(self,string:str) -> requests.Response:

        headers = {
            "User-Agent" : _UA,
            "Sec-Ch-Ua" : _SEC_CH_UA,
            "Content-Type" : "application/x-www-form-urlencoded",
            "Authorization" : "Bearer " + self.get_auth_bearer(),
            "X-Reddit-Loid" : self.session.cookies['loid'],
            "X-Reddit-Session" :  self.session.cookies['session_tracker']
        }

        payl = f"api_type=json&description={quote(string)}"

        return requests.post("https://oauth.reddit.com/api/appeal?redditWebClient=desktop2x&app=desktop2x-client-production&raw_json=1&gilding_detail=1",data=payl,headers=headers)

    def get_uh(self) -> str:
        resp = self.session.get("https://www.reddit.com/prefs/apps/")
        soup = BeautifulSoup(resp.content,'html.parser')
        return soup.find("input",{'name':'uh'})['value'] #type: ignore
    
    def create_app(self,name:str='test',app_type:str='script',desc:str='',about_url:str='',redir_uri:str=_LOCALHOST) -> tuple[str,str]:
        clid,clsecret = "",""
        uh = self.get_uh()
        payl = f"uh={uh}&name={name}&app_type={app_type}&description={desc}&about_url={about_url}&redirect_uri={redir_uri}&id=%23create-app&renderstyle=html"
        resp = self.session.post("https://www.reddit.com/api/updateapp",data=payl)
        if resp.json()["success"]:
            field = resp.json()["jquery"]
            print(field)
            for id1,id2,vtype,v in field:
                if id1 == 22 and id2 == 23 and vtype == "call":
                    clid,clsecret = re.search(_CLIENT_ID_REGX,v[0]).group(1),re.search(_CLIENT_SECRET_REGX,v[0]).group(1) #type: ignore
            return clid,clsecret
        else:
            raise Exception(f"{resp.json()}")
        
