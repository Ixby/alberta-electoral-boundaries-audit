import{_ as e,d as t,h as n,i as r,m as i,r as a,s as o,u as s,v as c,x as l}from"./adxvj54q.js";var u={inject:{"vs:#decl":`
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
`}},d={inject:{"vs:#decl":`
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
`}},f={getDashArray:{type:`accessor`,value:[0,0]},getOffset:{type:`accessor`,value:0},dashJustified:!1,dashGapPickable:!1},p=class extends a{constructor({dash:e=!1,offset:t=!1,highPrecisionDash:n=!1}={}){super({dash:e||n,offset:t,highPrecisionDash:n})}isEnabled(e){return`pathTesselator`in e.state}getShaders(e){if(!e.isEnabled(this))return null;let t={};return e.opts.dash&&(t=o(t,u)),e.opts.offset&&(t=o(t,d)),t}initializeState(e,t){let n=this.getAttributeManager();!n||!t.isEnabled(this)||(t.opts.dash&&n.addInstanced({instanceDashArrays:{size:2,accessor:`getDashArray`},instanceDashOffsets:t.opts.highPrecisionDash?{size:1,accessor:`getPath`,transform:t.getDashOffsets.bind(this)}:{size:1,update:e=>{e.constant=!0,e.value=[0]}}}),t.opts.offset&&n.addInstanced({instanceOffsets:{size:1,accessor:`getOffset`}}))}updateState(e,t){if(!t.isEnabled(this))return;let n={};t.opts.dash&&(n.dashAlignMode=+!!this.props.dashJustified,n.dashGapPickable=!!this.props.dashGapPickable),this.state.model?.setUniforms(n)}getDashOffsets(t){let n=[0],r=this.props.positionFormat===`XY`?2:3,i=Array.isArray(t[0]),a=i?t.length:t.length/r,o,s;for(let c=0;c<a-1;c++)o=i?t[c]:t.slice(c*r,c*r+r),o=this.projectPosition(o),c>0&&(n[c]=n[c-1]+e(s,o)),s=o;return n[a-1]=0,n}};p.defaultProps=f,p.extensionName=`PathStyleExtension`;var m={name:`mask`,dependencies:[i],vs:`
uniform vec4 mask_bounds;
uniform bool mask_maskByInstance;
vec2 mask_getCoords(vec4 position) {
return (position.xy - mask_bounds.xy) / (mask_bounds.zw - mask_bounds.xy);
}
`,fs:`
uniform sampler2D mask_texture;
uniform int mask_channel;
uniform bool mask_enabled;
uniform bool mask_inverted;
bool mask_isInBounds(vec2 texCoords) {
if (!mask_enabled) {
return true;
}
vec4 maskColor = texture(mask_texture, texCoords);
float maskValue = 1.0;
if (mask_channel == 0) {
maskValue = maskColor.r;
} else if (mask_channel == 1) {
maskValue = maskColor.g;
} else if (mask_channel == 2) {
maskValue = maskColor.b;
} else if (mask_channel == 3) {
maskValue = maskColor.a;
}
if (mask_inverted) {
return maskValue >= 0.5;
} else {
return maskValue < 0.5;
}
}
`,inject:{"vs:#decl":`
out vec2 mask_texCoords;
`,"vs:#main-end":`
vec4 mask_common_position;
if (mask_maskByInstance) {
mask_common_position = project_position(vec4(geometry.worldPosition, 1.0));
} else {
mask_common_position = geometry.position;
}
mask_texCoords = mask_getCoords(mask_common_position);
`,"fs:#decl":`
in vec2 mask_texCoords;
`,"fs:#main-start":`
if (mask_enabled) {
bool mask = mask_isInBounds(mask_texCoords);
fragColor = texture(mask_texture, mask_texCoords);
if (!mask) discard;
}
`},getUniforms:e=>e&&`maskMap`in e?{mask_texture:e.maskMap}:{}},h={blendColorOperation:`subtract`,blendColorSrcFactor:`zero`,blendColorDstFactor:`one`,blendAlphaOperation:`subtract`,blendAlphaSrcFactor:`zero`,blendAlphaDstFactor:`one`},g=class extends t{constructor(e,t){super(e,t);let{mapSize:n=2048}=t;this.maskMap=e.createTexture({format:`rgba8unorm`,width:n,height:n,sampler:{minFilter:`linear`,magFilter:`linear`,addressModeU:`clamp-to-edge`,addressModeV:`clamp-to-edge`}}),this.fbo=e.createFramebuffer({id:`maskmap`,width:n,height:n,colorAttachments:[this.maskMap]})}render(e){let t=2**e.channel,n=[255,255,255,255];super.render({...e,clearColor:n,colorMask:t,target:this.fbo,pass:`mask`})}getLayerParameters(e,t,n){return{...e.props.parameters,blend:!0,depthTest:!1,...h}}shouldDrawLayer(e){return e.props.operation.includes(`mask`)}delete(){this.fbo.delete(),this.maskMap.delete()}};function _(e,t){let n=[1/0,1/0,-1/0,-1/0];for(let r of e){let e=r.getBounds();if(e){let i=r.projectPosition(e[0],{viewport:t,autoOffset:!1}),a=r.projectPosition(e[1],{viewport:t,autoOffset:!1});n[0]=Math.min(n[0],i[0]),n[1]=Math.min(n[1],i[1]),n[2]=Math.max(n[2],a[0]),n[3]=Math.max(n[3],a[1])}}return Number.isFinite(n[0])?n:null}var v=2048;function y(e){let{bounds:t,viewport:n,border:i=0}=e,{isGeospatial:a}=n;if(t[2]<=t[0]||t[3]<=t[1])return null;let o=n.unprojectPosition([(t[0]+t[2])/2,(t[1]+t[3])/2,0]),{width:c,height:l,zoom:u}=e;if(u===void 0){c-=i*2,l-=i*2;let e=Math.min(c/(t[2]-t[0]),l/(t[3]-t[1]));u=Math.min(Math.log2(e),20)}else if(!c||!l){let e=2**u;c=Math.round(Math.abs(t[2]-t[0])*e),l=Math.round(Math.abs(t[3]-t[1])*e);let n=v-i*2;if(c>n||l>n){let e=n/Math.max(c,l);c=Math.round(c*e),l=Math.round(l*e),u+=Math.log2(e)}}return a?new s({id:n.id,x:i,y:i,width:c,height:l,longitude:o[0],latitude:o[1],zoom:u,orthographic:!0}):new r({id:n.id,x:i,y:i,width:c,height:l,target:o,zoom:u,flipY:!1})}function b(e,t){let n;if(t&&t.length===2){let[r,i]=t,a=e.getBounds({z:r}),o=e.getBounds({z:i});n=[Math.min(a[0],o[0]),Math.min(a[1],o[1]),Math.max(a[2],o[2]),Math.max(a[3],o[3])]}else n=e.getBounds();let r=e.projectPosition(n.slice(0,2)),i=e.projectPosition(n.slice(2,4));return[r[0],r[1],i[0],i[1]]}function x(e,t,n){if(!e)return[0,0,1,1];let r=S(b(t,n));return e[2]-e[0]<=r[2]-r[0]&&e[3]-e[1]<=r[3]-r[1]?e:[Math.max(e[0],r[0]),Math.max(e[1],r[1]),Math.min(e[2],r[2]),Math.min(e[3],r[3])]}function S(e){let t=e[2]-e[0],n=e[3]-e[1],r=(e[0]+e[2])/2,i=(e[1]+e[3])/2;return[r-t,i-n,r+t,i+n]}var C=class{constructor(){this.id=`mask-effect`,this.props=null,this.useInPicking=!0,this.order=0,this.channels=[],this.masks=null}setup({device:e}){this.dummyMaskMap=e.createTexture({width:1,height:1}),this.maskPass=new g(e,{id:`default-mask`}),this.maskMap=this.maskPass.maskMap}preRender({layers:e,layerFilter:t,viewports:n,onViewportActive:r,views:i,isPicking:a}){let o=!1;if(a)return{didRender:o};let s=e.filter(e=>e.props.visible&&e.props.operation.includes(`mask`));if(s.length===0)return this.masks=null,this.channels.length=0,{didRender:o};this.masks={};let c=this._sortMaskChannels(s),u=n[0],d=!this.lastViewport||!this.lastViewport.equals(u);if(u.resolution!==void 0)return l.warn(`MaskExtension is not supported in GlobeView`)(),{didRender:o};for(let e in c){let n=this._renderChannel(c[e],{layerFilter:t,onViewportActive:r,views:i,viewport:u,viewportChanged:d});o||=n}return{didRender:o}}_renderChannel(e,{layerFilter:t,onViewportActive:n,views:r,viewport:i,viewportChanged:a}){let o=!1,s=this.channels[e.index];if(!s)return o;let l=e===s||e.layers.length!==s.layers.length||e.layers.some((e,t)=>e!==s.layers[t]||e.props.transitions)||e.layerBounds.some((e,t)=>e!==s.layerBounds[t]);if(e.bounds=s.bounds,e.maskBounds=s.maskBounds,this.channels[e.index]=e,l||a){this.lastViewport=i;let a=_(e.layers,i);if(e.bounds=a&&x(a,i),l||!c(e.bounds,s.bounds)){let{maskPass:s,maskMap:c}=this,l=a&&y({bounds:e.bounds,viewport:i,width:c.width,height:c.height,border:1});e.maskBounds=l?l.getBounds():[0,0,1,1],s.render({pass:`mask`,channel:e.index,layers:e.layers,layerFilter:t,viewports:l?[l]:[],onViewportActive:n,views:r,moduleParameters:{devicePixelRatio:1}}),o=!0}}return this.masks[e.id]={index:e.index,bounds:e.maskBounds,coordinateOrigin:e.coordinateOrigin,coordinateSystem:e.coordinateSystem},o}_sortMaskChannels(e){let t={},n=0;for(let r of e){let{id:e}=r.root,i=t[e];if(!i){if(++n>4){l.warn(`Too many mask layers. The max supported is 4`)();continue}i={id:e,index:this.channels.findIndex(t=>t?.id===e),layers:[],layerBounds:[],coordinateOrigin:r.root.props.coordinateOrigin,coordinateSystem:r.root.props.coordinateSystem},t[e]=i}i.layers.push(r),i.layerBounds.push(r.getBounds())}for(let e=0;e<4;e++){let n=this.channels[e];(!n||!(n.id in t))&&(this.channels[e]=null)}for(let e in t){let n=t[e];n.index<0&&(n.index=this.channels.findIndex(e=>!e),this.channels[n.index]=n)}return t}getModuleParameters(){return{maskMap:this.masks?this.maskMap:this.dummyMaskMap,maskChannels:this.masks}}cleanup(){this.dummyMaskMap&&=(this.dummyMaskMap.delete(),void 0),this.maskPass&&(this.maskPass.delete(),this.maskPass=void 0,this.maskMap=void 0),this.lastViewport=void 0,this.masks=null,this.channels.length=0}},w={maskId:``,maskByInstance:void 0,maskInverted:!1},T=class extends a{initializeState(){this.context.deck?._addDefaultEffect(new C)}getShaders(){let e=`instancePositions`in this.getAttributeManager().attributes;return this.props.maskByInstance!==void 0&&(e=!!this.props.maskByInstance),this.state.maskByInstance=e,{modules:[m]}}draw({uniforms:e,context:t,moduleParameters:r}){e.mask_maskByInstance=this.state.maskByInstance;let{maskId:i,maskInverted:a}=this.props,{maskChannels:o}=r,{viewport:s}=t;if(o&&o[i]){let{index:t,bounds:r,coordinateOrigin:c}=o[i],{coordinateSystem:l}=o[i];e.mask_enabled=!0,e.mask_channel=t,e.mask_inverted=a,l===n.DEFAULT&&(l=s.isGeospatial?n.LNGLAT:n.CARTESIAN);let u={modelMatrix:null,fromCoordinateOrigin:c,fromCoordinateSystem:l},d=this.projectPosition([r[0],r[1],0],u),f=this.projectPosition([r[2],r[3],0],u);e.mask_bounds=[d[0],d[1],f[0],f[1]]}else i&&l.warn(`Could not find a mask layer with id: ${i}`)(),e.mask_enabled=!1}};T.defaultProps=w,T.extensionName=`MaskExtension`;export{T as MaskExtension,p as PathStyleExtension};