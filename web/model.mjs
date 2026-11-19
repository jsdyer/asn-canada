export function total(dist){return Object.values(dist).reduce((acc,v)=>acc+v,0)}
export function selectedCount(row,family){return (family==='v6'?0:total(row[3]))+(family==='v4'?0:total(row[4]))}
export function matches(rows,query,view,family,sort){
 const term=query.trim().replace(/^as\s*(?=\d)/i,'').toLowerCase();
 const filtered=rows.filter(r=>(!term||String(r[0])===term||r[1].toLowerCase().includes(term))&&(view==='all'||r[2]===(view==='yes'))&&(family==='both'||selectedCount(r,family)>0));
 return filtered.sort((a,b)=>(sort==='size'?selectedCount(b,family)-selectedCount(a,family):sort==='name'?a[1].localeCompare(b[1]):0)||a[0]-b[0]);
}
