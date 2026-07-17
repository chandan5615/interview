let p=1,t=1;
async function load(){let r=await fetch('/products?page='+p);let d=await r.json();t=d.pages;document.getElementById('pg').innerText=` ${p}/${t} `;let b=document.getElementById('body');b.innerHTML='';d.data.forEach(x=>b.innerHTML+=`<tr><td>${x.name}</td><td>${x.stock}</td></tr>`);}
async function call(u){await fetch(u,{method:'POST'});p=1;load();}
function prev(){if(p>1){p--;load();}}
function next(){if(p<t){p++;load();}}
load();