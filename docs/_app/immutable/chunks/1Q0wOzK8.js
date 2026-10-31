import{A as e,O as t,S as n,T as r,X as i,a,h as o,n as s,y as c}from"./DlInTrtT.js";import{t as l}from"./DfCDyo-e.js";var u=class{static get componentName(){return Object.prototype.hasOwnProperty.call(this,`extensionName`)?this.extensionName:``}constructor(e){e&&(this.opts=e)}equals(e){return this===e||this.constructor===e.constructor&&a(this.opts,e.opts,1)}getShaders(e){return null}getSubLayerProps(e){let{defaultProps:t}=e.constructor,n={updateTriggers:{}};for(let e in t)if(e in this.props){let r=t[e],i=this.props[e];n[e]=i,r&&r.type===`accessor`&&(n.updateTriggers[e]=this.props.updateTriggers[e],typeof i==`function`&&(n[e]=this.getSubLayerAccessor(i)))}return n}initializeState(e,t){}updateState(e,t){}onNeedsRedraw(e){}getNeedsPickingBuffer(e){return!1}draw(e,t){}finalizeState(e,t){}};u.defaultProps={},u.extensionName=`LayerExtension`;var d={inject:{"vs:#decl":`
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
`}},f={inject:{"vs:#decl":`
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
`}},p={getDashArray:{type:`accessor`,value:[0,0]},getOffset:{type:`accessor`,value:0},dashJustified:!1,dashGapPickable:!1},m=class extends u{constructor({dash:e=!1,offset:t=!1,highPrecisionDash:n=!1}={}){super({dash:e||n,offset:t,highPrecisionDash:n})}isEnabled(e){return`pathTesselator`in e.state}getShaders(e){if(!e.isEnabled(this))return null;let t={};return e.opts.dash&&(t=l(t,d)),e.opts.offset&&(t=l(t,f)),t}initializeState(e,t){let n=this.getAttributeManager();!n||!t.isEnabled(this)||(t.opts.dash&&n.addInstanced({instanceDashArrays:{size:2,accessor:`getDashArray`},instanceDashOffsets:t.opts.highPrecisionDash?{size:1,accessor:`getPath`,transform:t.getDashOffsets.bind(this)}:{size:1,update:e=>{e.constant=!0,e.value=[0]}}}),t.opts.offset&&n.addInstanced({instanceOffsets:{size:1,accessor:`getOffset`}}))}updateState(e,t){if(!t.isEnabled(this))return;let n={};t.opts.dash&&(n.dashAlignMode=+!!this.props.dashJustified,n.dashGapPickable=!!this.props.dashGapPickable),this.state.model?.setUniforms(n)}getDashOffsets(e){let n=[0],r=this.props.positionFormat===`XY`?2:3,i=Array.isArray(e[0]),a=i?e.length:e.length/r,o,s;for(let c=0;c<a-1;c++)o=i?e[c]:e.slice(c*r,c*r+r),o=this.projectPosition(o),c>0&&(n[c]=n[c-1]+t(s,o)),s=o;return n[a-1]=0,n}};m.defaultProps=p,m.extensionName=`PathStyleExtension`;var h={name:`mask`,dependencies:[n],vs:`
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
`},getUniforms:e=>e&&`maskMap`in e?{mask_texture:e.maskMap}:{}},g={blendColorOperation:`subtract`,blendColorSrcFactor:`zero`,blendColorDstFactor:`one`,blendAlphaOperation:`subtract`,blendAlphaSrcFactor:`zero`,blendAlphaDstFactor:`one`},_=class extends c{constructor(e,t){super(e,t);let{mapSize:n=2048}=t;this.maskMap=e.createTexture({format:`rgba8unorm`,width:n,height:n,sampler:{minFilter:`linear`,magFilter:`linear`,addressModeU:`clamp-to-edge`,addressModeV:`clamp-to-edge`}}),this.fbo=e.createFramebuffer({id:`maskmap`,width:n,height:n,colorAttachments:[this.maskMap]})}render(e){let t=2**e.channel,n=[255,255,255,255];super.render({...e,clearColor:n,colorMask:t,target:this.fbo,pass:`mask`})}getLayerParameters(e,t,n){return{...e.props.parameters,blend:!0,depthTest:!1,...g}}shouldDrawLayer(e){return e.props.operation.includes(`mask`)}delete(){this.fbo.delete(),this.maskMap.delete()}};function v(e,t){let n=[1/0,1/0,-1/0,-1/0];for(let r of e){let e=r.getBounds();if(e){let i=r.projectPosition(e[0],{viewport:t,autoOffset:!1}),a=r.projectPosition(e[1],{viewport:t,autoOffset:!1});n[0]=Math.min(n[0],i[0]),n[1]=Math.min(n[1],i[1]),n[2]=Math.max(n[2],a[0]),n[3]=Math.max(n[3],a[1])}}return Number.isFinite(n[0])?n:null}var y=2048;function b(e){let{bounds:t,viewport:n,border:r=0}=e,{isGeospatial:i}=n;if(t[2]<=t[0]||t[3]<=t[1])return null;let a=n.unprojectPosition([(t[0]+t[2])/2,(t[1]+t[3])/2,0]),{width:c,height:l,zoom:u}=e;if(u===void 0){c-=r*2,l-=r*2;let e=Math.min(c/(t[2]-t[0]),l/(t[3]-t[1]));u=Math.min(Math.log2(e),20)}else if(!c||!l){let e=2**u;c=Math.round(Math.abs(t[2]-t[0])*e),l=Math.round(Math.abs(t[3]-t[1])*e);let n=y-r*2;if(c>n||l>n){let e=n/Math.max(c,l);c=Math.round(c*e),l=Math.round(l*e),u+=Math.log2(e)}}return i?new o({id:n.id,x:r,y:r,width:c,height:l,longitude:a[0],latitude:a[1],zoom:u,orthographic:!0}):new s({id:n.id,x:r,y:r,width:c,height:l,target:a,zoom:u,flipY:!1})}function x(e,t){let n;if(t&&t.length===2){let[r,i]=t,a=e.getBounds({z:r}),o=e.getBounds({z:i});n=[Math.min(a[0],o[0]),Math.min(a[1],o[1]),Math.max(a[2],o[2]),Math.max(a[3],o[3])]}else n=e.getBounds();let r=e.projectPosition(n.slice(0,2)),i=e.projectPosition(n.slice(2,4));return[r[0],r[1],i[0],i[1]]}function S(e,t,n){if(!e)return[0,0,1,1];let r=C(x(t,n));return e[2]-e[0]<=r[2]-r[0]&&e[3]-e[1]<=r[3]-r[1]?e:[Math.max(e[0],r[0]),Math.max(e[1],r[1]),Math.min(e[2],r[2]),Math.min(e[3],r[3])]}function C(e){let t=e[2]-e[0],n=e[3]-e[1],r=(e[0]+e[2])/2,i=(e[1]+e[3])/2;return[r-t,i-n,r+t,i+n]}var w=class{constructor(){this.id=`mask-effect`,this.props=null,this.useInPicking=!0,this.order=0,this.channels=[],this.masks=null}setup({device:e}){this.dummyMaskMap=e.createTexture({width:1,height:1}),this.maskPass=new _(e,{id:`default-mask`}),this.maskMap=this.maskPass.maskMap}preRender({layers:e,layerFilter:t,viewports:n,onViewportActive:r,views:a,isPicking:o}){let s=!1;if(o)return{didRender:s};let c=e.filter(e=>e.props.visible&&e.props.operation.includes(`mask`));if(c.length===0)return this.masks=null,this.channels.length=0,{didRender:s};this.masks={};let l=this._sortMaskChannels(c),u=n[0],d=!this.lastViewport||!this.lastViewport.equals(u);if(u.resolution!==void 0)return i.warn(`MaskExtension is not supported in GlobeView`)(),{didRender:s};for(let e in l){let n=this._renderChannel(l[e],{layerFilter:t,onViewportActive:r,views:a,viewport:u,viewportChanged:d});s||=n}return{didRender:s}}_renderChannel(t,{layerFilter:n,onViewportActive:r,views:i,viewport:a,viewportChanged:o}){let s=!1,c=this.channels[t.index];if(!c)return s;let l=t===c||t.layers.length!==c.layers.length||t.layers.some((e,t)=>e!==c.layers[t]||e.props.transitions)||t.layerBounds.some((e,t)=>e!==c.layerBounds[t]);if(t.bounds=c.bounds,t.maskBounds=c.maskBounds,this.channels[t.index]=t,l||o){this.lastViewport=a;let o=v(t.layers,a);if(t.bounds=o&&S(o,a),l||!e(t.bounds,c.bounds)){let{maskPass:e,maskMap:c}=this,l=o&&b({bounds:t.bounds,viewport:a,width:c.width,height:c.height,border:1});t.maskBounds=l?l.getBounds():[0,0,1,1],e.render({pass:`mask`,channel:t.index,layers:t.layers,layerFilter:n,viewports:l?[l]:[],onViewportActive:r,views:i,moduleParameters:{devicePixelRatio:1}}),s=!0}}return this.masks[t.id]={index:t.index,bounds:t.maskBounds,coordinateOrigin:t.coordinateOrigin,coordinateSystem:t.coordinateSystem},s}_sortMaskChannels(e){let t={},n=0;for(let r of e){let{id:e}=r.root,a=t[e];if(!a){if(++n>4){i.warn(`Too many mask layers. The max supported is 4`)();continue}a={id:e,index:this.channels.findIndex(t=>t?.id===e),layers:[],layerBounds:[],coordinateOrigin:r.root.props.coordinateOrigin,coordinateSystem:r.root.props.coordinateSystem},t[e]=a}a.layers.push(r),a.layerBounds.push(r.getBounds())}for(let e=0;e<4;e++){let n=this.channels[e];(!n||!(n.id in t))&&(this.channels[e]=null)}for(let e in t){let n=t[e];n.index<0&&(n.index=this.channels.findIndex(e=>!e),this.channels[n.index]=n)}return t}getModuleParameters(){return{maskMap:this.masks?this.maskMap:this.dummyMaskMap,maskChannels:this.masks}}cleanup(){this.dummyMaskMap&&=(this.dummyMaskMap.delete(),void 0),this.maskPass&&(this.maskPass.delete(),this.maskPass=void 0,this.maskMap=void 0),this.lastViewport=void 0,this.masks=null,this.channels.length=0}},T={maskId:``,maskByInstance:void 0,maskInverted:!1},E=class extends u{initializeState(){this.context.deck?._addDefaultEffect(new w)}getShaders(){let e=`instancePositions`in this.getAttributeManager().attributes;return this.props.maskByInstance!==void 0&&(e=!!this.props.maskByInstance),this.state.maskByInstance=e,{modules:[h]}}draw({uniforms:e,context:t,moduleParameters:n}){e.mask_maskByInstance=this.state.maskByInstance;let{maskId:a,maskInverted:o}=this.props,{maskChannels:s}=n,{viewport:c}=t;if(s&&s[a]){let{index:t,bounds:n,coordinateOrigin:i}=s[a],{coordinateSystem:l}=s[a];e.mask_enabled=!0,e.mask_channel=t,e.mask_inverted=o,l===r.DEFAULT&&(l=c.isGeospatial?r.LNGLAT:r.CARTESIAN);let u={modelMatrix:null,fromCoordinateOrigin:i,fromCoordinateSystem:l},d=this.projectPosition([n[0],n[1],0],u),f=this.projectPosition([n[2],n[3],0],u);e.mask_bounds=[d[0],d[1],f[0],f[1]]}else a&&i.warn(`Could not find a mask layer with id: ${a}`)(),e.mask_enabled=!1}};E.defaultProps=T,E.extensionName=`MaskExtension`;export{E as MaskExtension,m as PathStyleExtension};