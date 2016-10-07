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

//生成数组
function range(){
	var start=0,
		end,
		inc=1;
	if(arguments.length==1){end=arguments[0]};
	if(arguments.length==2){start=arguments[0];end=arguments[1]}
	if(arguments.length==3){start=arguments[0];end=arguments[1];inc=arguments[2]}

	var arr=[];
	for(var i=start;i<end;i+=inc){
		arr.push(i);
	}
	return arr;
}
//插入排序
function insert_sort(arr){
	function iter(sortedArray,i){
		if(i==arr.length){return sortedArray};
		var temp=arr[i];
		sortedArray[i]=arr[i]
		for(var j=i;j>0;j--){
			if(temp<sortedArray[j-1]){
				sortedArray[j]=sortedArray[j-1]; 
			}else{
				sortedArray[j]=temp;
				break;
			}
		};
		return iter(sortedArray,i+1)
	}
	return iter([],0)
}


//列出数组内所有元素
function list(array){
	return iter([],0,array)
}

//遍历数组array,生成一维数组
function iter(result,n,array){
	if(n==array.length){return result};
	if (array[n] instanceof Array){
		Array.prototype.push.apply(result,list(array[n]));
		return iter(result,n+1,array);
	}else{
		Array.prototype.push.call(result,array[n]);
		return iter(result,n+1,array);
	}
}
