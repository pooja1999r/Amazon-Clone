// alert('hello');


function bigImg(x){
        x.style.height = "70px";
        x.style.width ="70x";
}
function normalImg(x) {
    x.style.height = "50px";
    x.style.width ="50x";
}
function myFun1(x) {
 
  y=document.getElementById('popup1');
  if (y.style.display=="none") {
    x.style.color="blue";
    document.getElementById('popup1').style.display='block';
  }
  else{
    document.getElementById('popup1').style.display='none';
  }
  
} 
function myFun2(x) {
  
  y=document.getElementById('popup2');
  if (y.style.display=="none") {
    x.style.color="blue";
    document.getElementById('popup2').style.display='block';
  }
  else{
    document.getElementById('popup2').style.display='none';
  }
  
} 
function myFun3(x) {

  y=document.getElementById('popup3');
  if (y.style.display=="none") {
    x.style.color="blue";
    document.getElementById('popup3').style.display='block';
  }
  else{
    document.getElementById('popup3').style.display='none';
  }
  
} 
function myFun4(x) {

  y=document.getElementById('popup4');
 
  if (y.style.display=="none") {
    x.style.color="blue";
    document.getElementById('popup4').style.display='block';
  }
  else{
    document.getElementById('popup4').style.display='none';
  }
  
} 

