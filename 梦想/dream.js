var settings={
	operation: "GET",
	headers:{
			'Host': 'h5.weiyingonline.com',
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
			'Connection': 'keep-alive',
			'Upgrade-Insecure-Requests': '1',
			'Cookie': 'totoro_cookie=1484129147647_9300; totoro_share_click_cookie=1484129147638_1808; JSESSIONID=685BEB546B16CF9F86BA068B39BBA22D',
			'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_1_1 like Mac OS X) AppleWebKit/602.2.14 (KHTML, like Gecko) Mobile/14B100 MicroMessenger/6.5.3 NetType/WIFI Language/zh_CN',
			'Accept-Language': 'zh-cn',
			'Accept-Encoding': 'gzip, deflate',
			'Connection': 'keep-alive',
		}
}

DESKTOP_USER_AGENTS = [ "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
		'Mozilla/5.0 (X11; Linux x86_64; rv:29.0) Gecko/20100101 Firefox/29.0',
		'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/537.36',
		'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:29.0) Gecko/20100101 Firefox/29.0',
		'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/537.36',
		'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14',
		'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:29.0) Gecko/20100101 Firefox/29.0',
		'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/537.36',
		'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)',
		'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
		'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0)',
		'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
		'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
		'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
		'Mozilla/5.0 (iPhone; CPU iPhone OS 10_1_1 like Mac OS X) AppleWebKit/602.2.14 (KHTML, like Gecko) Mobile/14B100 MicroMessenger/6.5.3 NetType/WIFI Language/zh_CN'

	];

//循环访问直播网页	
var i=0;
//var phantom = require('phantom');
var webPage = require('webpage');
var page = webPage.create();
var url='http://h5.weiyingonline.com/share_play/SharePlayClickAction.a?shareDetailId=1182444'
var url='http://h5.weiyingonline.com/share_play/SharePlayClickAction.a?shareDetailId=1183885'
var url='http://h5.weiyingonline.com/share_play/SharePlayClickAction.a?shareDetailId=1184579'

var page;
function iter(){
	//随机产生user-agent
	//settings.headers['User-Agent']=DESKTOP_USER_AGENTS[Math.floor(Math.random()*7)]
	i=i+1;
	console.log(i);	
//	var page=null;
	page=null;
	page = webPage.create();
	page.open(url, settings,function (s) {
		console.log(s==='success');
		while(s!=="success"){
			console.log('wait a minute');
		}

	});
	if(i>=1000){phantom.exit();}
	setTimeout(arguments.callee, 1000)
}
iter()