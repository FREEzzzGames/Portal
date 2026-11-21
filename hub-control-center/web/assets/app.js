const $ = (id) => document.getElementById(id);
const fmtBytes = (n) => {
  if (n === null || n === undefined || !Number.isFinite(Number(n))) return "—";
  const units = ["B","KB","MB","GB","TB"]; let v = Number(n), i = 0;
  while (v >= 1024 && i < units.length - 1) { v /= 1024; i++; }
  return v.toFixed(i >= 3 ? 1 : 0) + " " + units[i];
};
const fmtDuration = (seconds) => {
  if (!Number.isFinite(seconds)) return "—";
  const d=Math.floor(seconds/86400), h=Math.floor(seconds%86400/3600), m=Math.floor(seconds%3600/60);
  return d ? d+"д "+h+"ч" : h+"ч "+m+"м";
};
const safe = (v) => String(v ?? "—").replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
const pct = (v) => Math.max(0,Math.min(100,Number(v)||0));
const setMetric = (valueId,barId,footId,value,foot) => {
  $(valueId).innerHTML = Math.round(value) + "<small>%</small>";
  $(barId).style.width = pct(value)+"%";
  $(footId).textContent = foot;
};
function showToast(message){const el=$("toast");el.textContent=message;el.classList.add("show");setTimeout(()=>el.classList.remove("show"),2600);}
function navigate(page){
  if(page==="more"){showToast("Дополнительные модули доступны в боковом меню на компьютере.");return;}
  document.querySelectorAll(".page").forEach(x=>x.classList.toggle("active",x.id==="page-"+page));
  document.querySelectorAll("[data-page]").forEach(x=>x.classList.toggle("active",x.dataset.page===page));
  const titles={home:"Обзор системы",services:"Сервисы и контейнеры",system:"Система",development:"Разработка",smart:"Умный дом",ai:"AI Center"};
  $("page-title").textContent=titles[page]||"FREEzzz HUB";
}
document.addEventListener("click",e=>{
  const nav=e.target.closest("[data-page]"); if(nav){navigate(nav.dataset.page);return;}
  const open=e.target.closest("[data-open]"); if(open) navigate(open.dataset.open);
});
function renderContainers(data){
  const list=data.containers||[];
  $("container-count").textContent=list.length;
  $("services-count").textContent=list.length+" шт.";
  $("docker-state").textContent=data.available?"Docker доступен":"Docker недоступен";
  $("docker-detail").textContent=data.available?"Обнаружено контейнеров: "+list.length:(data.reason||"Нет доступа к Docker API");
  const row=(c)=>'<div class="container-row"><div style="min-width:0"><div class="container-name">'+safe(c.name)+'</div><div class="container-sub">'+safe(c.image)+' · '+safe(c.status)+'</div></div><span class="state-pill '+(c.state==="running"?"":"off")+'">'+safe(c.state).toUpperCase()+'</span></div>';
  $("container-preview").innerHTML=list.length?list.slice(0,4).map(row).join(""):'<div class="empty-state">Контейнеры не обнаружены</div>';
  $("containers-full").innerHTML=list.length?list.map(row).join(""):'<div class="empty-state">Нет доступных контейнеров. '+safe(data.reason||"")+'</div>';
}
function renderSystem(s){
  $("side-host").textContent=s.host||"unknown"; $("hero-host").textContent=s.host||"Сервер";
  $("hero-platform").textContent=s.platform||"Linux";
  $("uptime").textContent=fmtDuration(s.uptime_seconds);
  $("updated").textContent=new Date(s.observed_at).toLocaleTimeString("ru-RU");
  const cpu=s.cpu||{},mem=s.memory||{},swap=s.swap||{},disk=s.storage||{};
  setMetric("cpu-value","cpu-bar","cpu-foot",cpu.percent||0,(cpu.logical_cores??"—")+" логических ядер");
  setMetric("ram-value","ram-bar","ram-foot",mem.percent||0,fmtBytes(mem.used)+" / "+fmtBytes(mem.total));
  setMetric("disk-value","disk-bar","disk-foot",disk.root_percent||0,fmtBytes(disk.root_used)+" / "+fmtBytes(disk.root_total));
  setMetric("swap-value","swap-bar","swap-foot",swap.percent||0,fmtBytes(swap.used)+" / "+fmtBytes(swap.total));
  $("detail-host").textContent=s.host||"—"; $("detail-arch").textContent=s.platform||"—";
  $("detail-kernel").textContent=s.kernel||"—"; $("detail-cores").textContent=cpu.logical_cores??"—";
  $("detail-load").textContent=Array.isArray(s.load_average)?s.load_average.map(x=>Number(x).toFixed(2)).join(" / "):"—";
  $("sys-cpu").textContent=(cpu.percent??"—")+"%";
  $("sys-ram").textContent=(mem.percent??"—")+"%"; $("sys-ram-detail").textContent=fmtBytes(mem.used)+" used / "+fmtBytes(mem.total);
  $("sys-swap").textContent=(swap.percent??"—")+"%"; $("sys-swap-detail").textContent=fmtBytes(swap.used)+" used / "+fmtBytes(swap.total);
  $("sys-disk").textContent=(disk.root_percent??"—")+"%"; $("sys-disk-detail").textContent=fmtBytes(disk.root_free)+" free / "+fmtBytes(disk.root_total);
  const rows=[["Host",s.host],["OS",s.platform],["Kernel",s.kernel],["CPU cores",cpu.logical_cores],["RAM total",fmtBytes(mem.total)],["Swap total",fmtBytes(swap.total)],["Root filesystem",fmtBytes(disk.root_total)],["Network TX",fmtBytes(s.network?.bytes_sent)],["Network RX",fmtBytes(s.network?.bytes_recv)]];
  $("system-details").innerHTML=rows.map(([a,b])=>'<div><span>'+safe(a)+'</span><b>'+safe(b)+'</b></div>').join("");
}
async function refresh(){
  $("api-state").textContent="Обновление";
  try{
    const response=await fetch("/api/v1/overview",{cache:"no-store"});
    if(!response.ok)throw new Error("HTTP "+response.status);
    const data=await response.json();
    renderSystem(data.system);renderContainers(data.docker);
    $("api-dot").className="dot ok";$("api-state").textContent="Backend online";
  }catch(err){
    $("api-dot").className="dot bad";$("api-state").textContent="Нет связи";
    showToast("Не удалось получить данные: "+err.message);
  }
}
$("refresh").addEventListener("click",refresh);
function tick(){ $("clock").textContent=new Date().toLocaleTimeString("ru-RU");}
tick();setInterval(tick,1000);refresh();setInterval(refresh,5000);
