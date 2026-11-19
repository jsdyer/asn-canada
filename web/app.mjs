import {get,node,options,data,fmt,stats,table,barlist,link,csv,initial,share,failure} from './ui.mjs';
import {matches,total} from './model.mjs';
let rows=[], filtered=[], preferred=initial.get('network')||'852';
const controls=['query','view','family','sort','network'];
function render(){
 filtered=matches(rows,get('query').value,get('view').value,get('family').value,get('sort').value);
 const old=preferred;options('network',filtered.map(r=>[r[0],'AS'+r[0]+' · '+(r[1]||'Unnamed registration')]),old);
 preferred=get('network').value;
 const row=filtered.find(r=>String(r[0])===preferred);
 get('title').textContent=row?'AS'+row[0]+' · '+(row[1]||'Unnamed registration'):'No matching network';
 get('meaning').textContent=row?(row[2]?'RIPEstat lists this registration as routed.':'RIPEstat lists this registration as unrouted.'):'Try another search or broaden the filters.';
 get('links').replaceChildren();
 if(row){
  stats([[fmt(total(row[3])),'Visible IPv4 prefixes'],[fmt(total(row[4])),'Visible IPv6 prefixes']]);
  const lengths=get('family').value==='v4'?[[4,row[3]]]:get('family').value==='v6'?[[6,row[4]]]:[[4,row[3]],[6,row[4]]];
  const bars=lengths.flatMap(([family,dist])=>Object.entries(dist).map(([len,num])=>['IPv'+family+' /'+len,num]));barlist('lengths',bars);
  if(!bars.length)get('lengths').textContent='No non-default prefix met the ten-peer threshold.';
  get('links').append(link('RIPEstat for AS'+row[0],'https://stat.ripe.net/AS'+row[0]),' · ',link('Published prefixes','https://stat.ripe.net/data/announced-prefixes/data.json?resource=AS'+row[0]));
 }else{stats([]);barlist('lengths',[])}
 get('matches').textContent=fmt(filtered.length)+' registrations match. The table shows up to 100. The selector and CSV include every match.';
 table('records',['Network','Name','Registry visibility','IPv4 prefixes','IPv6 prefixes'],filtered.slice(0,100).map(r=>{
 const a=link('AS'+r[0],'?network='+r[0]);a.addEventListener('click',e=>{e.preventDefault();preferred=String(r[0]);render();get('title').scrollIntoView({block:'center'})});
 return [a,r[1]||'Unnamed',r[2]?'Routed':'Unrouted',fmt(total(r[3])),fmt(total(r[4]))]
 }));share(controls);
}
async function start(){const [state,list]=await Promise.all([data('status'),data('networks')]);rows=list;
 get('stamp').textContent=fmt(state.count)+' Canadian registrations · RIPEstat '+state.registry+' · IPv4 RIS '+state.v4+' · IPv6 RIS '+state.v6+' · Retrieved '+state.retrieved;
 for(const id of controls.slice(0,-1)){const el=get(id),v=initial.get(id);if(v&&(id==='query'||[...el.options].some(o=>o.value===v)))el.value=v;el.addEventListener(id==='query'?'input':'change',render)}
 get('network').addEventListener('change',()=>{preferred=get('network').value;render()});
 get('export').onclick=()=>csv('canadian-asns',['ASN','Network','Routed in country report','IPv4 prefixes','IPv6 prefixes'],filtered.map(r=>[r[0],r[1],r[2],total(r[3]),total(r[4])]));render()}
start().catch(failure);
