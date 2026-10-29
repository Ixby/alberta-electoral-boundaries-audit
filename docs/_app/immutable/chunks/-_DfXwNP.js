import{E as e,i as t}from"./CpRBtFxl.js";import{t as n}from"./DfCDyo-e.js";var r=class{static get componentName(){return Object.prototype.hasOwnProperty.call(this,`extensionName`)?this.extensionName:``}constructor(e){e&&(this.opts=e)}equals(e){return this===e||this.constructor===e.constructor&&t(this.opts,e.opts,1)}getShaders(e){return null}getSubLayerProps(e){let{defaultProps:t}=e.constructor,n={updateTriggers:{}};for(let e in t)if(e in this.props){let r=t[e],i=this.props[e];n[e]=i,r&&r.type===`accessor`&&(n.updateTriggers[e]=this.props.updateTriggers[e],typeof i==`function`&&(n[e]=this.getSubLayerAccessor(i)))}return n}initializeState(e,t){}updateState(e,t){}onNeedsRedraw(e){}getNeedsPickingBuffer(e){return!1}draw(e,t){}finalizeState(e,t){}};r.defaultProps={},r.extensionName=`LayerExtension`;var i={inject:{"vs:#decl":`
in vec2 instanceDashArrays;
in float instanceDashOffsets;
out vec2 vDashArray;
out float vDashOffset;
`,"vs:#main-end":`
vDashArray = instanceDashArrays;
vDashOffset = instanceDashOffsets / width.x;
`,"fs:#decl":`
uniform float dashAlignMode;
uniform float capType;
uniform bool dashGapPickable;
in vec2 vDashArray;
in float vDashOffset;
`,"fs:#main-start":`
float solidLength = vDashArray.x;
float gapLength = vDashArray.y;
float unitLength = solidLength + gapLength;
float offset;
if (unitLength > 0.0) {
if (dashAlignMode == 0.0) {
offset = vDashOffset;
} else {
unitLength = vPathLength / round(vPathLength / unitLength);
offset = solidLength / 2.0;
}
float unitOffset = mod(vPathPosition.y + offset, unitLength);
if (gapLength > 0.0 && unitOffset > solidLength) {
if (capType <= 0.5) {
if (!(dashGapPickable && bool(picking.isActive))) {
discard;
}
} else {
float distToEnd = length(vec2(
min(unitOffset - solidLength, unitLength - unitOffset),
vPathPosition.x
));
if (distToEnd > 1.0) {
if (!(dashGapPickable && bool(picking.isActive))) {
discard;
}
}
}
}
}
`}},a={inject:{"vs:#decl":`
in float instanceOffsets;
`,"vs:DECKGL_FILTER_SIZE":`
float offsetWidth = abs(instanceOffsets * 2.0) + 1.0;
size *= offsetWidth;
`,"vs:#main-end":`
float offsetWidth = abs(instanceOffsets * 2.0) + 1.0;
float offsetDir = sign(instanceOffsets);
vPathPosition.x = (vPathPosition.x + offsetDir) * offsetWidth - offsetDir;
vPathPosition.y *= offsetWidth;
vPathLength *= offsetWidth;
`,"fs:#main-start":`
float isInside;
isInside = step(-1.0, vPathPosition.x) * step(vPathPosition.x, 1.0);
if (isInside == 0.0) {
discard;
}
`}},o={getDashArray:{type:`accessor`,value:[0,0]},getOffset:{type:`accessor`,value:0},dashJustified:!1,dashGapPickable:!1},s=class extends r{constructor({dash:e=!1,offset:t=!1,highPrecisionDash:n=!1}={}){super({dash:e||n,offset:t,highPrecisionDash:n})}isEnabled(e){return`pathTesselator`in e.state}getShaders(e){if(!e.isEnabled(this))return null;let t={};return e.opts.dash&&(t=n(t,i)),e.opts.offset&&(t=n(t,a)),t}initializeState(e,t){let n=this.getAttributeManager();!n||!t.isEnabled(this)||(t.opts.dash&&n.addInstanced({instanceDashArrays:{size:2,accessor:`getDashArray`},instanceDashOffsets:t.opts.highPrecisionDash?{size:1,accessor:`getPath`,transform:t.getDashOffsets.bind(this)}:{size:1,update:e=>{e.constant=!0,e.value=[0]}}}),t.opts.offset&&n.addInstanced({instanceOffsets:{size:1,accessor:`getOffset`}}))}updateState(e,t){if(!t.isEnabled(this))return;let n={};t.opts.dash&&(n.dashAlignMode=+!!this.props.dashJustified,n.dashGapPickable=!!this.props.dashGapPickable),this.state.model?.setUniforms(n)}getDashOffsets(t){let n=[0],r=this.props.positionFormat===`XY`?2:3,i=Array.isArray(t[0]),a=i?t.length:t.length/r,o,s;for(let c=0;c<a-1;c++)o=i?t[c]:t.slice(c*r,c*r+r),o=this.projectPosition(o),c>0&&(n[c]=n[c-1]+e(s,o)),s=o;return n[a-1]=0,n}};s.defaultProps=o,s.extensionName=`PathStyleExtension`;export{s as PathStyleExtension};