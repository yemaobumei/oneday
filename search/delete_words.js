//用来删除一个文本内容里的空行和空begin-end对
/*如
123
23
begin

	begin
	end
	232
end
2323*/

var test=["1","2","begin","","","end","3","begin","end","begin","end","4"];
function trim(arr){
	blank_line(arr);
	while(1){
		if(del(arr)==0){
			break;
		}
	}
	return arr;
}

//删除所有空行，空字符
function blank_line(arr){
	var i=0;
	while(1){
		if(arr[i]==""){
			arr.splice(i,1);
		}else{
			i+=1;
		}
		if(i>=arr.length-1){
			break;
		}
	}
}
//遍历一次数组删除紧挨着的begin-end对。
function del(arr){
	var j=0;//记录删除begin-end对的次数
	var i=0;
	while(1){
		if(arr[i]==="begin" && arr[i+1]==="end"){
			arr.splice(i,2);
			j=j+1;
		}else{
			i+=1;
		}

		if(i>=arr.length-1){
			break;
		}
	}
	return j;
}
console.log(trim(test))