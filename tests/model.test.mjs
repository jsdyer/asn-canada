import test from 'node:test';
import assert from 'node:assert/strict';
import {matches,selectedCount} from '../web/model.mjs';
const r=[[852,'TELUS',true,{'16':2},{'32':1}],[1,'Other',false,{},{}]];
test('accepts exact ASN, mixed-case name and registry filters',()=>{assert.equal(matches(r,'as852','all','both','asn')[0][0],852);assert.equal(matches(r,'tel','yes','v6','size').length,1);assert.equal(matches(r,'','no','v4','asn').length,0)});
test('families preserve threshold zero and add independently',()=>{assert.equal(selectedCount(r[0],'both'),3);assert.equal(selectedCount(r[1],'v6'),0)});
