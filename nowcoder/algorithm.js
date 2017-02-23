 //1-----------------------------------------------------------------------------------
 //重建二叉树
 // 输入某二叉树的前序遍历和中序遍历的结果，请重建出该二叉树。
 //假设输入的前序遍历和中序遍历的结果中都不含重复的数字。
 //例如输入前序遍历序列{1,2,4,7,3,5,6,8}和中序遍历序列{4,7,2,1,5,3,8,6}，则重建二叉树并返回。
 function TreeNode(x) {
	this.val = x;
	this.left = null;
	this.right = null;
}
//返回0层treenode 
function reConstructBinaryTree(pre, vin)
{
		if(pre.length>0){
			var root=pre[0];
			if(pre.length==1){
				return new TreeNode(root);
			}
			var vin_root_index=vin.indexOf(root);//root在中根序中的位置
			var vin_left=vin.slice(0,vin_root_index);
			var vin_right=vin.slice(1+vin_root_index);
			var len_vin_left=vin_left.length;
			var len_vin_right=vin_right.length;
			var pre_left=pre.slice(1,1+len_vin_left);
			var pre_right=pre.slice(1+len_vin_left);
			var t=new TreeNode(root);
			t.left=reConstructBinaryTree(pre_left,vin_left);
			t.right=reConstructBinaryTree(pre_right,vin_right);
			return t;          
		}else{
			return null;
		}        			
}
//二叉树的宽度遍历
function wide_traversal(rootNode){
	var queue=[rootNode];
	var currentNode;
	var sequence=[];
	while(true){
		currentNode=queue.shift();
		if(currentNode===undefined){
			return sequence;
		}
		sequence.push(currentNode.val);
		if(currentNode.left){
			queue.push(currentNode.left)
		}
		if(currentNode.right){
			queue.push(currentNode.right)
		}
	}
}

//2-----------------------------------------------------------------------------------
//用两个栈来实现一个队列，完成队列的Push和Pop操作。 队列中的元素为int类型。
function Stack(){
    var item=[];
    this.push=function(x){
       return item.push(x);
    };
    this.pop=function(){
        return item.pop();
    };
    this.isEmpty=function(){
        return item.length==0;
    };
}
function Queue(){
	var stack1=new Stack();
	var stack2=new Stack();
	this.push=function(node){
		return stack1.push(node);
	}
	this.pop=function(){
		if(stack2.isEmpty()){
			while(!stack1.isEmpty()){
				stack2.push(stack1.pop());
			}	
		}
		return stack2.pop();
	}	
}

//3-----------------------------------------------------------------------------------
//输出斐波那契数列的第n项。
//方法1比较耗内存。stack
var Fib=function(){
			var seq={
			    '0':0,
			    '1':1,
			}
			var Fibonacci=function (n)
						{
							if(seq[n]!=undefined){
						        return seq[n];
						    }
						    var f1=Fibonacci(n-2);
						    var f2=Fibonacci(n-1);
						    var f3=f1+f2;
						    seq[n-2]=f1;
						    seq[n-1]=f2;
						    seq[n]=f3;
						    return f3;
						}
			return Fibonacci;	
		}()
//方法2比较节省内存
var Fib2=function(){
			var seq={
			    '0':0,
			    '1':1,
			}
			var Fibonacci=function (n)
						{
							if(seq[n]!=undefined){
						        return seq[n];
						    }
						    var f1=0;
						    var f2=1;
						    var f3;
						    var i=2;
						    while(i<=n){
						    	f3=f1+f2;
						    	seq[i]=f3	
						    	i+=1;
						    	f1=f2;
						    	f2=f3;
						    }
						    return f3;
						}
			return Fibonacci;	
		}()


