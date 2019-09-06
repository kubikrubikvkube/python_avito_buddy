import random

common_user_agents = [
    "Mozilla/5.0 (Linux; Android 7.0; Redmi Note 4 Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; U; Android 4.2.2;pl-pl; Lenovo S5000-F/JDQ39) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.2.2 Mobile Safari/534.30",
    "Mozilla/5.0 (Linux; Android 6.0.1; MotoG3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.80 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 7.0; HUAWEI VNS-L23) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.80 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 5.1.1; ASUS_X00BD Build/LMY47V) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 7.1.1; Moto G Play) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 6.0; HUAWEI VNS-L21 Build/HUAWEIVNS-L21) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.111 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 6.0; CRO-L23 Build/HUAWEICRO-L23) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 7.0; Moto G (5) Build/NPPS25.137-93-8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.109 Mobile Safari/537.36",
    "Mozilla/5.0 (Android 9; Mobile; rv:68.0) Gecko/68.0 Firefox/68.0",
    "Mozilla/5.0 (Linux; Android 4.4.2; G735-L03 Build/HuaweiG735-L03) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 6.0; MotoG3 Build/MPIS24.65-33.1-2-16) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 7.0; Moto C Plus) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.80 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 7.1.1; ASUS_X00ID Build/NMF26F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 7.1.1; ASUS_X00ID Build/NMF26F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.91 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 7.0; PRA-LX1 Build/HUAWEIPRA-LX1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.111 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 7.1.1; Moto X Play Build/NPD26.48-24-1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 7.1.1; Moto G Play) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.64 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 7.0; Moto G (4) Build/NPJS25.93-14-10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.111 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 8.0.0; ASUS_Z012DC) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.80 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 7.1.1; Moto G (5S) Plus Build/NPSS26.116-26-18) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 7.0; Moto G (4) Build/NPJS25.93-14-18) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.137 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 6.0; LENNY3 Build/MRA58K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.85 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 8.1.0; Moto G (5)) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Mobile Safari/537.36",
    "Mozilla/5.0 (Android 7.0; Mobile; rv:62.0) Gecko/62.0 Firefox/62.0",
    "Mozilla/5.0 (Linux; Android 8.1.0; Moto G (5) Build/OPP28.85-16) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 5.1; HUAWEI CUN-L23 Build/HUAWEICUN-L23) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.91 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 7.0; G3313) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.80 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 6.0; MotoG3 Build/MPIS24.65-33.1-2-10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.132 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 8.0.0; ANE-LX3 Build/HUAWEIANE-LX3; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/69.0.3497.100 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 6.0.1; Moto G Play Build/MPIS24.241-15.3-26) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 7.0; F3113 Build/33.3.A.1.97) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 8.0.0; RNE-L03 Build/HUAWEIRNE-L03) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 7.0; BLL-L23) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.80 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 7.1.1; Moto Z2 Play Build/NPSS26.118-19-1-2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.111 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 7.0; Moto G (5) Build/NPPS25.137-93-8-2-2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 7.0; TRT-LX3 Build/HUAWEITRT-LX3; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/69.0.3497.100 Mobile Safari/537.36 [FB_IAB/FB4A;FBAV/192.0.0.34.85;]",
    "Mozilla/5.0 (Linux; Android 4.2.2; Trooper_X40 Build/Trooper_X40) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.76 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 7.0; Moto G (5) Build/NPPS25.137-93-4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 4.4.4; E2105 Build/24.0.A.5.14) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.83 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 5.1; HUAWEI LUA-L03 Build/HUAWEILUA-L03) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 6.0; MYA-L23) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.80 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 7.1.2; AFTMM Build/NS6264; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/59.0.3071.125 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 7.1.2; AFTMM Build/NS6265; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/70.0.3538.110 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 7.1; Mi A1 Build/N2G47H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.83 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 5.1; A37f Build/LMY47V) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.93 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 6.0.1; CPH1607 Build/MMB29M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/63.0.3239.111 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 5.1.1; Lenovo-A6020l36 Build/LMY47V) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.93 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 4.3; MediaPad 7 Youth 2 Build/HuaweiMediaPad) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.83 Safari/537.36",
    "Dalvik/2.1.0 (Linux; U; Android 5.1.1; AFTT Build/LVY48F) CTV",
    "Mozilla/5.0 (Linux; Android 6.0.1; Redmi 4A Build/MMB29M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/60.0.3112.116 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 6.0.1; Lenovo-A6020l36 Build/MMB29M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.93 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; U; Android 6.0.1; zh-CN; F5121 Build/34.0.A.1.247) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.5.1.944 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 6.0; MYA-L22 Build/HUAWEIMYA-L22) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.84 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 5.1; A1601 Build/LMY47I) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.98 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 7.0; TRT-LX2 Build/HUAWEITRT-LX2; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/59.0.3071.125 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 6.0; CAM-L21 Build/HUAWEICAM-L21; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/62.0.3202.84 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 7.1.2; Redmi 4X Build/N2G47H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.111 Mobile Safari/537.36"
]


class UserAgentProvider:
    @staticmethod
    def provide() -> str:
        return random.choice(common_user_agents)


available_proxies = [
    "https://qabE6F:LzWcpL@45.95.151.204:8000/",
    "https://qabE6F:LzWcpL@45.95.149.81:8000/",
    "https://qabE6F:LzWcpL@45.95.149.155:8000/",
    "https://qabE6F:LzWcpL@45.95.151.52:8000/",
    "https://sdM3k6:A8LV6t@45.135.29.251:8000/",
]


class ProxyProvider:
    @staticmethod
    def provide() -> str:
        return random.choice(available_proxies)
