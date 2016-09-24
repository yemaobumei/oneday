function sum(n){
	if(n===0){
		return 0
	}
	return n+sum(n-1)
}

function sum(n){
	function iter(i,result){
		if(i===0){
			return result
		}
		return iter(i-1,result+i)
	}
	return iter(n,0)

}

function f(str){
	if(str.length==1){return str+1}
	var count=1;
	for(var i=1;i<str.length;i++){
		if(str[0]==str[i]){
			count=count+1;
		}else{
			return str[0]+count+f(str.slice(i))
		}
	}
	return str[0]+count;

}
function isHuiwen(str){
	if (str.length<=1){
		return true
	}else{
		if(str.length==2){return str[0]==str[1]}
		if(str[0]==str[str.length-1]){
			return isHuiwen(str.slice(1,str.length-1));
		}
		return false;
	}
}

function quchong(arr){
	for(var i=1;i<arr.length;i++){
			if arr[0]==arr[i]{
				return quchong(arr.slice(1))
			}else{
				return quchong
			}
	}

}

function sorts(arr){
	arr.sort(function(a,b){return a-b});
	function quchong(li){
		if(li.length==1){return li};
		return li[0]==li[1]?quchong(li.slice(1)):[li[0]].concat(quchong(li.slice(1)));
	}
	return quchong(arr);
}
