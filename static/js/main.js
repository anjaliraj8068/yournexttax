const ctx=document.getElementById('incomeChart');

if(ctx){

new Chart(ctx,{

type:'bar',

data:{

labels:[
'Salary',
'Business',
'Capital Gain',
'Other'
],

datasets:[{

label:'Income',

data:[0,0,0,0]

}]

}

});

}