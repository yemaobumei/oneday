// Firefox和Chrome早期版本中带有前缀
var MutationObserver = window.MutationObserver || window.WebKitMutationObserver || window.MozMutationObserver

// 选择目标节点
//var target = document.querySelector('#chat-msg-list');
//var target = document.getElementById('chat-msg-list');
var target = document.getElementById('chat-list-ctnr');
var len=target.childNodes.length;

// 创建观察者对象
var observer = new MutationObserver(function(mutations) {
  mutations.forEach(function(mutation) {
	var target=mutation.target.childNodes;
	var len=target.length;
	var addedNodes=mutation.addedNodes;
    addedNodes.forEach(function(node){

    	//注意赠送礼物节点的区别，高于1000的节点的div与弹幕消息的class一致是.msg-item-ctnr，里层是.gift-msg;
    	//而低于1000的礼物的div的class是.gift-msg-item,
    	//所以find语句应用是须作判断
    	var $node=$(node);
    	if($node.hasClass('gift-msg-item')) {
    		thank($node,'.user-name-low','.gift-count','.action');//低于1000道具礼物
    	}else if($node.find('.gift-msg').length>0) {
    		thank($node.find('.gift-msg'),'.user-name','.gift-count','.action');
    	}else if($node.find('.guard-sys').length>0) {
    		welcome($node);	
    	}else if($node.find('.chat-msg').length>0) {
    		reply($node);
    	}   	
    });
  });    
});

//赠送礼物致谢
var gift_num=0;//记录礼物赠送次数
var  single_gift={};//{'x':1,'y':2}记录单个礼物赠送次数，提示不要刷屏
function thank($giftMsg,uname,giftCount,action) {
	if(gift_num%20==0){single_gift={}};
	if($giftMsg.length>0) {
		var uname=$giftMsg.find(uname).text();
		var count=$giftMsg.find(giftCount).text().match(/\d+/)[0];
		var action=$giftMsg.find(action).text();
		var response="谢谢"+uname+action+"x"+count;
		if(count=="1"){//赠送礼物x1，记录该用户。
			if(single_gift[uname]==undefined){
				single_gift[uname]=0;
			}
			single_gift[uname]+=1;
			if(single_gift[uname]>=5){//该用户累计多次单个礼物投送发出提醒.10次赠送礼物记录里该用户单次赠送了5次
				single_gift[uname]=0;
				sendDanmu(uname+',礼物请尽量打包投喂');
			}
		}
		if(parseInt(count)>=10||action.search('辣条')<0){
			sendDanmu(response);
		}
		
	}
}
//欢迎大佬进入房间
function welcome($node)	{
	var types=['.color','.welcome'];
	types.forEach(function(type){
		var $guardName=$node.find(type).text();;
		if($guardName.length>0){
			var response=$guardName+"晚上好";
			sendDanmu(response);
		}
	})
}
//弹幕礼仪
function reply($node){
	if(gift_num%40==0){sendDanmu("主播游戏这么厉害，不上波船吗。")};
	var uname=$node.find('.user-name').text();
	var msg=$node.find('.msg-content').text();
	if(uname=='[自己] : '){
		return;
	}
	var database={'背景音乐':'网易云ID:喵咭喵呜QAQ,关注有歌单','求bgm':'网易云ID:喵咭喵呜QAQ,关注有歌单','喵咭6666':'主播这么厉害不点拨关注吗',
	  '主播胸小':'请大家注意弹幕礼仪!','做鸡巴儿':'请大家注意弹幕礼仪','主播真菜':'这只是发挥失常，大家看久点就知道了',
	  '主播段位':'主播钻石水平，日常AD。想看什么英雄可以跟主播说',
	  '主播炸了':'主播加油，胜利在望，决不动摇',
	  '夜猫大佬gay':'不要趁我不在就gay我',
	  'gay弹幕姬':'不要调戏我，会坏的',
	  '小姐姐漂亮':'喵咭和往常一样漂亮',
	  '主播漂亮':'喵咭和往常一样漂亮',
	  '主播修仙':'不要休闲哟，对身体不好呢',
	  '唱歌好听':'喵咭唱歌好听',
	  '废话在哪里呢':'废话被麻麻gank了',
	  '夜猫大佬不在了':'我与喵咭共存亡',	
	}
	$.each(database,function(key,val){
		if(msg.search(key)>-1){
			sendDanmu(val);
			return;			
		}else if(compare(key.split(''),msg.split(''))>=45.0){
			sendDanmu(val);
			return;	
		}

	})
}
//发送弹幕消息
function sendDanmu(danmu)	{
	gift_num+=1;
	$('#danmu-textbox').val(danmu);
	$('#danmu-send-btn').click();
}

// 配置观察选项:
var config = { attributes: true, childList: true, characterData: true, subtree:true}

// 传入目标节点和观察选项
observer.observe(target, config);
 
// 随后,你还可以停止观察
//observer.disconnect();




function compare(x, y) {
    var z = 0;
    var s = x.length + y.length;;
 
    x.sort();
    y.sort();
    var a = x.shift();
    var b = y.shift();
 
    while(a !== undefined && b !== undefined) {
        if (a === b) {
            z++;
            a = x.shift();
            b = y.shift();
        } else if (a < b) {
            a = x.shift();
        } else if (a > b) {
            b = y.shift();
        }
    }
    return z/s * 200;
}