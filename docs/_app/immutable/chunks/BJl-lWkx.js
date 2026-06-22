import{A as e,E as t,O as n,T as r,b as i,f as a,h as o,i as s,l as c,m as l,p as u,r as d,s as f,u as p,x as m,y as h}from"./BS4EHaZ3.js";var ee=`
uniform bool brushing_enabled;
uniform int brushing_target;
uniform vec2 brushing_mousePos;
uniform float brushing_radius;
in vec2 brushingTargets;
out float brushing_isVisible;
bool brushing_isPointInRange(vec2 position) {
if (!brushing_enabled) {
return true;
}
vec2 source_commonspace = project_position(position);
vec2 target_commonspace = project_position(brushing_mousePos);
float distance = length((target_commonspace - source_commonspace) / project_uCommonUnitsPerMeter.xy);
return distance <= brushing_radius;
}
bool brushing_arePointsInRange(vec2 sourcePos, vec2 targetPos) {
return brushing_isPointInRange(sourcePos) || brushing_isPointInRange(targetPos);
}
void brushing_setVisible(bool visible) {
brushing_isVisible = float(visible);
}
`,te=`
uniform bool brushing_enabled;
in float brushing_isVisible;
`,ne={source:0,target:1,custom:2,source_target:3},g={name:`brushing`,dependencies:[h],vs:ee,fs:te,inject:{"vs:DECKGL_FILTER_GL_POSITION":`
vec2 brushingTarget;
vec2 brushingSource;
if (brushing_target == 3) {
brushingTarget = geometry.worldPositionAlt.xy;
brushingSource = geometry.worldPosition.xy;
} else if (brushing_target == 0) {
brushingTarget = geometry.worldPosition.xy;
} else if (brushing_target == 1) {
brushingTarget = geometry.worldPositionAlt.xy;
} else {
brushingTarget = brushingTargets;
}
bool visible;
if (brushing_target == 3) {
visible = brushing_arePointsInRange(brushingSource, brushingTarget);
} else {
visible = brushing_isPointInRange(brushingTarget);
}
brushing_setVisible(visible);
`,"fs:DECKGL_FILTER_COLOR":`
    if (brushing_enabled && brushing_isVisible < 0.5) {
      discard;
    }
  `},getUniforms:e=>{if(!e||!(`viewport`in e))return{};let{brushingEnabled:t=!0,brushingRadius:n=1e4,brushingTarget:r=`source`,mousePosition:i,viewport:a}=e;return{brushing_enabled:!!(t&&i&&a.containsPixel(i)),brushing_radius:n,brushing_target:ne[r]||0,brushing_mousePos:i?a.unproject([i.x-a.x,i.y-a.y]):[0,0]}}},re={getBrushingTarget:{type:`accessor`,value:[0,0]},brushingTarget:`source`,brushingEnabled:!0,brushingRadius:1e4},_=class extends d{getShaders(){return{modules:[g]}}initializeState(e,t){let n=this.getAttributeManager();n&&n.add({brushingTargets:{size:2,stepMode:`dynamic`,accessor:`getBrushingTarget`}});let r=()=>{this.getCurrentLayer()?.setNeedsRedraw()};this.state.onMouseMove=r,e.deck&&e.deck.eventManager.on({pointermove:r,pointerleave:r})}finalizeState(e,t){if(e.deck){let t=this.state.onMouseMove;e.deck.eventManager.off({pointermove:t,pointerleave:t})}}};_.defaultProps=re,_.extensionName=`BrushingExtension`;var v=`
uniform bool filter_useSoftMargin;
uniform bool filter_enabled;
uniform bool filter_transformSize;
uniform ivec4 filter_categoryBitMask;
#ifdef DATAFILTER_TYPE
uniform DATAFILTER_TYPE filter_min;
uniform DATAFILTER_TYPE filter_softMin;
uniform DATAFILTER_TYPE filter_softMax;
uniform DATAFILTER_TYPE filter_max;
in DATAFILTER_TYPE filterValues;
#ifdef DATAFILTER_DOUBLE
in DATAFILTER_TYPE filterValues64Low;
uniform DATAFILTER_TYPE filter_min64High;
uniform DATAFILTER_TYPE filter_max64High;
#endif
#endif
#ifdef DATACATEGORY_TYPE
in DATACATEGORY_TYPE filterCategoryValues;
#endif
out float dataFilter_value;
float dataFilter_reduceValue(float value) {
return value;
}
float dataFilter_reduceValue(vec2 value) {
return min(value.x, value.y);
}
float dataFilter_reduceValue(vec3 value) {
return min(min(value.x, value.y), value.z);
}
float dataFilter_reduceValue(vec4 value) {
return min(min(value.x, value.y), min(value.z, value.w));
}
#ifdef DATAFILTER_TYPE
void dataFilter_setValue(DATAFILTER_TYPE valueFromMin, DATAFILTER_TYPE valueFromMax) {
if (filter_useSoftMargin) {
DATAFILTER_TYPE leftInRange = mix(
smoothstep(filter_min, filter_softMin, valueFromMin),
step(filter_min, valueFromMin),
step(filter_softMin, filter_min)
);
DATAFILTER_TYPE rightInRange = mix(
1.0 - smoothstep(filter_softMax, filter_max, valueFromMax),
step(valueFromMax, filter_max),
step(filter_max, filter_softMax)
);
dataFilter_value = dataFilter_reduceValue(leftInRange * rightInRange);
} else {
dataFilter_value = dataFilter_reduceValue(
step(filter_min, valueFromMin) * step(valueFromMax, filter_max)
);
}
}
#endif
#ifdef DATACATEGORY_TYPE
void dataFilter_setCategoryValue(DATACATEGORY_TYPE category) {
#if DATACATEGORY_CHANNELS == 1
int dataFilter_masks = filter_categoryBitMask[int(category / 32.0)];
#elif DATACATEGORY_CHANNELS == 2
ivec2 dataFilter_masks = ivec2(
filter_categoryBitMask[int(category.x / 32.0)],
filter_categoryBitMask[int(category.y / 32.0) + 2]
);
#elif DATACATEGORY_CHANNELS == 3
ivec3 dataFilter_masks = filter_categoryBitMask.xyz;
#else
ivec4 dataFilter_masks = filter_categoryBitMask;
#endif
DATACATEGORY_TYPE dataFilter_bits = DATACATEGORY_TYPE(dataFilter_masks) / pow(DATACATEGORY_TYPE(2.0), mod(category, 32.0));
dataFilter_bits = mod(floor(dataFilter_bits), 2.0);
#if DATACATEGORY_CHANNELS == 1
if(dataFilter_bits == 0.0) dataFilter_value = 0.0;
#else
if(any(equal(dataFilter_bits, DATACATEGORY_TYPE(0.0)))) dataFilter_value = 0.0;
#endif
}
#endif
`,y=`
uniform bool filter_transformColor;
in float dataFilter_value;
`;function b(e){if(!e||!(`extensions`in e))return{};let{filterRange:t=[-1,1],filterEnabled:n=!0,filterTransformSize:r=!0,filterTransformColor:i=!0}=e,a=e.filterSoftRange||t;return{...Number.isFinite(t[0])?{filter_min:t[0],filter_softMin:a[0],filter_softMax:a[1],filter_max:t[1]}:{filter_min:t.map(e=>e[0]),filter_softMin:a.map(e=>e[0]),filter_softMax:a.map(e=>e[1]),filter_max:t.map(e=>e[1])},filter_enabled:n,filter_useSoftMargin:!!e.filterSoftRange,filter_transformSize:n&&r,filter_transformColor:n&&i}}function x(e){if(!e||!(`extensions`in e))return{};let t=b(e);if(Number.isFinite(t.filter_min)){let e=Math.fround(t.filter_min);t.filter_min-=e,t.filter_softMin-=e,t.filter_min64High=e;let n=Math.fround(t.filter_max);t.filter_max-=n,t.filter_softMax-=n,t.filter_max64High=n}else{let e=t.filter_min.map(Math.fround);t.filter_min=t.filter_min.map((t,n)=>t-e[n]),t.filter_softMin=t.filter_softMin.map((t,n)=>t-e[n]),t.filter_min64High=e;let n=t.filter_max.map(Math.fround);t.filter_max=t.filter_max.map((e,t)=>e-n[t]),t.filter_softMax=t.filter_softMax.map((e,t)=>e-n[t]),t.filter_max64High=n}return t}var S={"vs:#main-start":`
dataFilter_value = 1.0;
if (filter_enabled) {
#ifdef DATAFILTER_TYPE
#ifdef DATAFILTER_DOUBLE
dataFilter_setValue(
filterValues - filter_min64High + filterValues64Low,
filterValues - filter_max64High + filterValues64Low
);
#else
dataFilter_setValue(filterValues, filterValues);
#endif
#endif
#ifdef DATACATEGORY_TYPE
dataFilter_setCategoryValue(filterCategoryValues);
#endif
}
`,"vs:#main-end":`
if (dataFilter_value == 0.0) {
gl_Position = vec4(0.);
}
`,"vs:DECKGL_FILTER_SIZE":`
if (filter_transformSize) {
size = size * dataFilter_value;
}
`,"fs:DECKGL_FILTER_COLOR":`
if (dataFilter_value == 0.0) discard;
if (filter_transformColor) {
color.a *= dataFilter_value;
}
`},ie={name:`data-filter`,vs:v,fs:y,inject:S,getUniforms:b},ae={name:`data-filter-fp64`,vs:v,fs:y,inject:S,getUniforms:x},oe=`#version 300 es
#define SHADER_NAME data-filter-vertex-shader

#ifdef FLOAT_TARGET
  in float filterIndices;
  in float filterPrevIndices;
#else
  in vec2 filterIndices;
  in vec2 filterPrevIndices;
#endif

out vec4 vColor;
const float component = 1.0 / 255.0;

void main() {
  #ifdef FLOAT_TARGET
    dataFilter_value *= float(filterIndices != filterPrevIndices);
    gl_Position = vec4(0.0, 0.0, 0.0, 1.0);
    vColor = vec4(0.0, 0.0, 0.0, 1.0);
  #else
    // Float texture is not supported: pack result into 4 channels x 256 px x 64px
    dataFilter_value *= float(filterIndices.x != filterPrevIndices.x);
    float col = filterIndices.x;
    float row = filterIndices.y * 4.0;
    float channel = floor(row);
    row = fract(row);
    vColor = component * vec4(bvec4(channel == 0.0, channel == 1.0, channel == 2.0, channel == 3.0));
    gl_Position = vec4(col * 2.0 - 1.0, row * 2.0 - 1.0, 0.0, 1.0);
  #endif
  gl_PointSize = 1.0;
}
`,se=`#version 300 es
#define SHADER_NAME data-filter-fragment-shader
precision highp float;

in vec4 vColor;

out vec4 fragColor;

void main() {
  if (dataFilter_value < 0.5) {
    discard;
  }
  fragColor = vColor;
}
`,ce=[`float32-renderable-webgl`,`texture-blend-float-webgl`];function le(e){return ce.every(t=>e.features.has(t))}function ue(e,t){return t?e.createFramebuffer({width:1,height:1,colorAttachments:[e.createTexture({format:`rgba32float`,type:5126,mipmaps:!1})]}):e.createFramebuffer({width:256,height:64,colorAttachments:[e.createTexture({format:`rgba8unorm`,type:5126,mipmaps:!1})]})}function de(e,t,n){return t.defines.NON_INSTANCED_MODEL=1,n&&(t.defines.FLOAT_TARGET=1),new a(e,{id:`data-filter-aggregation-model`,vertexCount:1,isInstanced:!1,drawMode:0,vs:oe,fs:se,...t})}var fe={blend:!0,blendFunc:[1,1,1,1],blendEquation:[32774,32774],depthTest:!1},pe={getFilterValue:{type:`accessor`,value:0},getFilterCategory:{type:`accessor`,value:0},onFilteredItemsChange:{type:`function`,value:null,optional:!0},filterEnabled:!0,filterRange:[-1,1],filterSoftRange:null,filterCategories:[0],filterTransformSize:!0,filterTransformColor:!0},me={categorySize:0,filterSize:1,fp64:!1,countItems:!1},C={1:`float`,2:`vec2`,3:`vec3`,4:`vec4`},w=class extends d{constructor(e={}){super({...me,...e})}getShaders(e){let{categorySize:t,filterSize:n,fp64:r}=e.opts,i={};return t&&(i.DATACATEGORY_TYPE=C[t],i.DATACATEGORY_CHANNELS=t),n&&(i.DATAFILTER_TYPE=C[n],i.DATAFILTER_DOUBLE=!!r),{modules:[r?ae:ie],defines:i}}initializeState(e,t){let n=this.getAttributeManager(),{categorySize:r,filterSize:i,fp64:a}=t.opts;n&&(i&&n.add({filterValues:{size:i,type:a?`float64`:`float32`,stepMode:`dynamic`,accessor:`getFilterValue`}}),r&&n.add({filterCategoryValues:{size:r,stepMode:`dynamic`,accessor:`getFilterCategory`,transform:r===1?e=>t._getCategoryKey.call(this,e,0):e=>e.map((e,n)=>t._getCategoryKey.call(this,e,n))}}));let{device:o}=this.context;if(n&&t.opts.countItems){let e=le(o);n.add({filterIndices:{size:e?1:2,vertexOffset:1,type:`unorm8`,accessor:(t,{index:n})=>{let r=t&&t.__source?t.__source.index:n;return e?(r+1)%255:[(r+1)%255,Math.floor(r/255)%255]},shaderAttributes:{filterPrevIndices:{vertexOffset:0},filterIndices:{vertexOffset:1}}}});let r=ue(o,e),i=de(o,t.getShaders.call(this,t),e);this.setState({filterFBO:r,filterModel:i})}}updateState({props:e,oldProps:t,changeFlags:n},r){let i=this.getAttributeManager(),{categorySize:a}=r.opts;if(this.state.filterModel){let n=i.attributes.filterValues?.needsUpdate()||i.attributes.filterCategoryValues?.needsUpdate()||e.filterEnabled!==t.filterEnabled||e.filterRange!==t.filterRange||e.filterSoftRange!==t.filterSoftRange||e.filterCategories!==t.filterCategories;n&&this.setState({filterNeedsUpdate:n})}i?.attributes.filterCategoryValues&&((i.attributes.filterCategoryValues.needsUpdate()||!c(e.filterCategories,t.filterCategories,2))&&this.setState({categoryBitMask:null}),n.dataChanged&&(this.setState({categoryMap:Array(a).fill(0).map(()=>({}))}),i.attributes.filterCategoryValues.setNeedsUpdate(`categoryMap`)))}draw(e,t){let n=this.state.filterFBO,r=this.state.filterModel,i=this.state.filterNeedsUpdate,{onFilteredItemsChange:a}=this.props;if(this.state.categoryBitMask||t._updateCategoryBitMask.call(this,e,t),e.uniforms.filter_categoryBitMask=this.state.categoryBitMask,i&&a&&r){let{attributes:{filterValues:t,filterCategoryValues:i,filterIndices:o}}=this.getAttributeManager();r.setVertexCount(this.getNumInstances()),this.context.device.clearWebGL({framebuffer:n,color:[0,0,0,0]}),r.updateModuleSettings(e.moduleParameters),r.setAttributes({...t?.getValue(),...i?.getValue(),...o?.getValue()}),r.setUniforms(e.uniforms),r.device.withParametersWebGL({framebuffer:n,...fe,viewport:[0,0,n.width,n.height]},()=>{r.draw(this.context.renderPass)});let s=r.device.readPixelsToArrayWebGL(n),c=0;for(let e=0;e<s.length;e++)c+=s[e];a({id:this.id,count:c}),this.state.filterNeedsUpdate=!1}}finalizeState(){let e=this.state.filterFBO,t=this.state.filterModel;e?.destroy(),t?.destroy()}_updateCategoryBitMask(t,n){let{categorySize:r}=n.opts;if(!r)return;let{filterCategories:i}=this.props,a=new Uint32Array([0,0,0,0]),o=r===1?[i]:i,s=r===1?128:r===2?64:32;for(let t=0;t<o.length;t++){let r=o[t];for(let i of r){let r=n._getCategoryKey.call(this,i,t);if(r<s){let e=s/32*t+Math.floor(r/32);a[e]+=2**(r%32)}else e.warn(`Exceeded maximum number of categories (${s})`)()}}this.state.categoryBitMask=a}_getCategoryKey(e,t){let n=this.state.categoryMap[t];return e in n||(n[e]=Object.keys(n).length),n[e]}};w.defaultProps=pe,w.extensionName=`DataFilterExtension`;var he=`const vec2 WORLD_SCALE_FP64 = vec2(81.4873275756836, 0.0000032873668232014097);
uniform vec2 project_uViewProjectionMatrixFP64[16];
void mercatorProject_fp64(vec4 lnglat_fp64, out vec2 out_val[2]) {
#if defined(NVIDIA_FP64_WORKAROUND)
out_val[0] = sum_fp64(radians_fp64(lnglat_fp64.xy), PI_FP64 * ONE);
#else
out_val[0] = sum_fp64(radians_fp64(lnglat_fp64.xy), PI_FP64);
#endif
out_val[1] = sum_fp64(PI_FP64,
log_fp64(tan_fp64(sum_fp64(PI_4_FP64, radians_fp64(lnglat_fp64.zw) / 2.0))));
return;
}
void project_position_fp64(vec4 position_fp64, out vec2 out_val[2]) {
vec2 pos_fp64[2];
mercatorProject_fp64(position_fp64, pos_fp64);
out_val[0] = mul_fp64(pos_fp64[0], WORLD_SCALE_FP64);
out_val[1] = mul_fp64(pos_fp64[1], WORLD_SCALE_FP64);
return;
}
void project_position_fp64(vec2 position, vec2 position64xyLow, out vec2 out_val[2]) {
vec4 position64xy = vec4(
position.x, position64xyLow.x,
position.y, position64xyLow.y);
project_position_fp64(position64xy, out_val);
}
vec4 project_common_position_to_clipspace_fp64(vec2 vertex_pos_modelspace[4]) {
vec2 vertex_pos_clipspace[4];
mat4_vec4_mul_fp64(project_uViewProjectionMatrixFP64, vertex_pos_modelspace,
vertex_pos_clipspace);
return vec4(
vertex_pos_clipspace[0].x,
vertex_pos_clipspace[1].x,
vertex_pos_clipspace[2].x,
vertex_pos_clipspace[3].x
);
}
vec4 project_position_to_clipspace(
vec3 position, vec3 position64xyLow, vec3 offset, out vec4 commonPosition
) {
vec2 offset64[4];
vec4_fp64(vec4(offset, 0.0), offset64);
float z = project_size(position.z);
vec2 projectedPosition64xy[2];
project_position_fp64(position.xy, position64xyLow.xy, projectedPosition64xy);
vec2 commonPosition64[4];
commonPosition64[0] = sum_fp64(offset64[0], projectedPosition64xy[0]);
commonPosition64[1] = sum_fp64(offset64[1], projectedPosition64xy[1]);
commonPosition64[2] = sum_fp64(offset64[2], vec2(z, 0.0));
commonPosition64[3] = vec2(1.0, 0.0);
commonPosition = vec4(projectedPosition64xy[0].x, projectedPosition64xy[1].x, z, 1.0);
return project_common_position_to_clipspace_fp64(commonPosition64);
}
vec4 project_position_to_clipspace(
vec3 position, vec3 position64xyLow, vec3 offset
) {
vec4 commonPosition;
return project_position_to_clipspace(
position, position64xyLow, offset, commonPosition
);
}
`,{fp64ify:ge,fp64ifyMatrix4:_e}=n,T={name:`project64`,dependencies:[h,n],vs:he,getUniforms:E},ve=i(D);function E(e){if(e&&`viewport`in e){let{viewProjectionMatrix:t,scale:n}=e.viewport;return ve({viewProjectionMatrix:t,scale:n})}return{}}function D({viewProjectionMatrix:e,scale:t}){let n=_e(e);return{project_uViewProjectionMatrixFP64:n,project64_uViewProjectionMatrix:n,project64_uScale:ge(t)}}var O=class extends d{getShaders(){let{coordinateSystem:e}=this.props;if(e!==m.LNGLAT&&e!==m.DEFAULT)throw Error(`fp64: coordinateSystem must be LNGLAT`);return{modules:[T]}}};O.extensionName=`Fp64Extension`;var k={inject:{"vs:#decl":`
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
`}},A={inject:{"vs:#decl":`
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
`}},j={getDashArray:{type:`accessor`,value:[0,0]},getOffset:{type:`accessor`,value:0},dashJustified:!1,dashGapPickable:!1},M=class extends d{constructor({dash:e=!1,offset:t=!1,highPrecisionDash:n=!1}={}){super({dash:e||n,offset:t,highPrecisionDash:n})}isEnabled(e){return`pathTesselator`in e.state}getShaders(e){if(!e.isEnabled(this))return null;let t={};return e.opts.dash&&(t=f(t,k)),e.opts.offset&&(t=f(t,A)),t}initializeState(e,t){let n=this.getAttributeManager();!n||!t.isEnabled(this)||(t.opts.dash&&n.addInstanced({instanceDashArrays:{size:2,accessor:`getDashArray`},instanceDashOffsets:t.opts.highPrecisionDash?{size:1,accessor:`getPath`,transform:t.getDashOffsets.bind(this)}:{size:1,update:e=>{e.constant=!0,e.value=[0]}}}),t.opts.offset&&n.addInstanced({instanceOffsets:{size:1,accessor:`getOffset`}}))}updateState(e,t){if(!t.isEnabled(this))return;let n={};t.opts.dash&&(n.dashAlignMode=+!!this.props.dashJustified,n.dashGapPickable=!!this.props.dashGapPickable),this.state.model?.setUniforms(n)}getDashOffsets(e){let t=[0],n=this.props.positionFormat===`XY`?2:3,i=Array.isArray(e[0]),a=i?e.length:e.length/n,o,s;for(let c=0;c<a-1;c++)o=i?e[c]:e.slice(c*n,c*n+n),o=this.projectPosition(o),c>0&&(t[c]=t[c-1]+r(s,o)),s=o;return t[a-1]=0,t}};M.defaultProps=j,M.extensionName=`PathStyleExtension`;var N=`
in vec4 fillPatternFrames;
in float fillPatternScales;
in vec2 fillPatternOffsets;
uniform bool fill_patternEnabled;
uniform vec2 fill_patternTextureSize;
out vec2 fill_uv;
out vec4 fill_patternBounds;
out vec4 fill_patternPlacement;
`,P=`
uniform bool fill_patternEnabled;
uniform bool fill_patternMask;
uniform sampler2D fill_patternTexture;
uniform vec2 fill_uvCoordinateOrigin;
uniform vec2 fill_uvCoordinateOrigin64Low;
in vec4 fill_patternBounds;
in vec4 fill_patternPlacement;
in vec2 fill_uv;
const float FILL_UV_SCALE = 512.0 / 40000000.0;
`,F={"vs:DECKGL_FILTER_GL_POSITION":`
fill_uv = geometry.position.xy;
`,"vs:DECKGL_FILTER_COLOR":`
if (fill_patternEnabled) {
fill_patternBounds = fillPatternFrames / vec4(fill_patternTextureSize, fill_patternTextureSize);
fill_patternPlacement.xy = fillPatternOffsets;
fill_patternPlacement.zw = fillPatternScales * fillPatternFrames.zw;
}
`,"fs:DECKGL_FILTER_COLOR":`
if (fill_patternEnabled) {
vec2 scale = FILL_UV_SCALE * fill_patternPlacement.zw;
vec2 patternUV = mod(mod(fill_uvCoordinateOrigin, scale) + fill_uvCoordinateOrigin64Low + fill_uv, scale) / scale;
patternUV = mod(fill_patternPlacement.xy + patternUV, 1.0);
vec2 texCoords = fill_patternBounds.xy + fill_patternBounds.zw * patternUV;
vec4 patternColor = texture(fill_patternTexture, texCoords);
color.a *= patternColor.a;
if (!fill_patternMask) {
color.rgb = patternColor.rgb;
}
}
`};function ye(e,t){if(!e)return{};if(`fillPatternTexture`in e){let{fillPatternTexture:t}=e;return{fill_patternTexture:t,fill_patternTextureSize:[t.width,t.height]}}if(`viewport`in e){let{fillPatternMask:n=!0,fillPatternEnabled:r=!0}=e,{project_uCommonOrigin:i}=t,a=[l(i[0]),l(i[1])];return{fill_uvCoordinateOrigin:i.slice(0,2),fill_uvCoordinateOrigin64Low:a,fill_patternMask:n,fill_patternEnabled:r}}return{}}var be={name:`fill-pattern`,vs:N,fs:P,inject:F,dependencies:[h],getUniforms:ye},xe={fillPatternEnabled:!0,fillPatternAtlas:{type:`image`,value:null,async:!0,parameters:{lodMaxClamp:0}},fillPatternMapping:{type:`object`,value:{},async:!0},fillPatternMask:!0,getFillPattern:{type:`accessor`,value:e=>e.pattern},getFillPatternScale:{type:`accessor`,value:1},getFillPatternOffset:{type:`accessor`,value:[0,0]}},I=class extends d{constructor({pattern:e=!1}={}){super({pattern:e})}isEnabled(e){return e.getAttributeManager()!==null&&!(`pathTesselator`in e.state)}getShaders(e){return e.isEnabled(this)?{modules:[e.opts.pattern&&be].filter(Boolean)}:null}initializeState(e,t){if(!t.isEnabled(this))return;let n=this.getAttributeManager();t.opts.pattern&&n.add({fillPatternFrames:{size:4,stepMode:`dynamic`,accessor:`getFillPattern`,transform:t.getPatternFrame.bind(this)},fillPatternScales:{size:1,stepMode:`dynamic`,accessor:`getFillPatternScale`,defaultValue:1},fillPatternOffsets:{size:2,stepMode:`dynamic`,accessor:`getFillPatternOffset`}}),this.setState({emptyTexture:this.context.device.createTexture({data:new Uint8Array(4),width:1,height:1})})}updateState({props:e,oldProps:t},n){n.isEnabled(this)&&e.fillPatternMapping&&e.fillPatternMapping!==t.fillPatternMapping&&this.getAttributeManager().invalidate(`getFillPattern`)}draw(e,t){if(!t.isEnabled(this))return;let{fillPatternAtlas:n}=this.props;this.setModuleParameters({fillPatternTexture:n||this.state.emptyTexture})}finalizeState(){this.state.emptyTexture?.delete()}getPatternFrame(e){let{fillPatternMapping:t}=this.getCurrentLayer().props,n=t&&t[e];return n?[n.x,n.y,n.width,n.height]:[0,0,0,0]}};I.defaultProps=xe,I.extensionName=`FillStyleExtension`;var Se={clipBounds:[0,0,1,1],clipByInstance:void 0},L=`
uniform vec4 clip_bounds;
bool clip_isInBounds(vec2 position) {
return position.x >= clip_bounds[0] && position.y >= clip_bounds[1] && position.x < clip_bounds[2] && position.y < clip_bounds[3];
}
`,Ce={name:`clip-vs`,vs:L},we={"vs:#decl":`
out float clip_isVisible;
`,"vs:DECKGL_FILTER_GL_POSITION":`
clip_isVisible = float(clip_isInBounds(geometry.worldPosition.xy));
`,"fs:#decl":`
in float clip_isVisible;
`,"fs:DECKGL_FILTER_COLOR":`
if (clip_isVisible < 0.5) discard;
`},Te={name:`clip-fs`,fs:L},Ee={"vs:#decl":`
out vec2 clip_commonPosition;
`,"vs:DECKGL_FILTER_GL_POSITION":`
clip_commonPosition = geometry.position.xy;
`,"fs:#decl":`
in vec2 clip_commonPosition;
`,"fs:DECKGL_FILTER_COLOR":`
if (!clip_isInBounds(clip_commonPosition)) discard;
`},R=class extends d{getShaders(){let e=`instancePositions`in this.getAttributeManager().attributes;return this.props.clipByInstance!==void 0&&(e=!!this.props.clipByInstance),this.state.clipByInstance=e,e?{modules:[Ce],inject:we}:{modules:[Te],inject:Ee}}draw({uniforms:e}){let{clipBounds:t}=this.props;if(this.state.clipByInstance)e.clip_bounds=t;else{let n=this.projectPosition([t[0],t[1],0]),r=this.projectPosition([t[2],t[3],0]);e.clip_bounds=[Math.min(n[0],r[0]),Math.min(n[1],r[1]),Math.max(n[0],r[0]),Math.max(n[1],r[1])]}}};R.defaultProps=Se,R.extensionName=`ClipExtension`;var De={name:`collision`,dependencies:[h],vs:`
in float collisionPriorities;
uniform sampler2D collision_texture;
uniform bool collision_sort;
uniform bool collision_enabled;
vec2 collision_getCoords(vec4 position) {
vec4 collision_clipspace = project_common_position_to_clipspace(position);
return (1.0 + collision_clipspace.xy / collision_clipspace.w) / 2.0;
}
float collision_match(vec2 tex, vec3 pickingColor) {
vec4 collision_pickingColor = texture(collision_texture, tex);
float delta = dot(abs(collision_pickingColor.rgb - pickingColor), vec3(1.0));
float e = 0.001;
return step(delta, e);
}
float collision_isVisible(vec2 texCoords, vec3 pickingColor) {
if (!collision_enabled) {
return 1.0;
}
const int N = 2;
float accumulator = 0.0;
vec2 step = vec2(1.0 / project_uViewportSize);
const float floatN = float(N);
vec2 delta = -floatN * step;
for(int i = -N; i <= N; i++) {
delta.x = -step.x * floatN;
for(int j = -N; j <= N; j++) {
accumulator += collision_match(texCoords + delta, pickingColor);
delta.x += step.x;
}
delta.y += step.y;
}
float W = 2.0 * floatN + 1.0;
return pow(accumulator / (W * W), 2.2);
}
`,inject:{"vs:#decl":`
float collision_fade = 1.0;
`,"vs:DECKGL_FILTER_GL_POSITION":`
if (collision_sort) {
float collisionPriority = collisionPriorities;
position.z = -0.001 * collisionPriority * position.w;
}
if (collision_enabled) {
vec4 collision_common_position = project_position(vec4(geometry.worldPosition, 1.0));
vec2 collision_texCoords = collision_getCoords(collision_common_position);
collision_fade = collision_isVisible(collision_texCoords, geometry.pickingColor / 255.0);
if (collision_fade < 0.0001) {
position = vec4(0.0, 0.0, 2.0, 1.0);
}
}
`,"vs:DECKGL_FILTER_COLOR":`
color.a *= collision_fade;
`},getUniforms:(e,t)=>{if(!e||!(`dummyCollisionMap`in e))return{};let{collisionFBO:n,drawToCollisionMap:r,dummyCollisionMap:i}=e;return{collision_sort:!!r,collision_texture:!r&&n?n.colorAttachments[0]:i}}},Oe=class extends o{renderCollisionMap(e,t){let n=[0,0,0,0],r=[1,1,e.width-2,e.height-2];this.render({...t,clearColor:n,scissorRect:r,target:e,pass:`collision`})}getLayerParameters(e,t,n){return{...e.props.parameters,blend:!1,depthRange:[0,1],depthTest:!0}}getModuleParameters(){return{drawToCollisionMap:!0,picking:{isActive:1,isAttribute:!1},lightSources:{}}}},z=2,ke=class{constructor(){this.id=`collision-filter-effect`,this.props=null,this.useInPicking=!0,this.order=1,this.channels={},this.collisionFBOs={}}setup(e){this.context=e;let{device:t}=e;this.dummyCollisionMap=t.createTexture({width:1,height:1}),this.collisionFilterPass=new Oe(t,{id:`default-collision-filter`})}preRender({effects:e,layers:t,layerFilter:n,viewports:r,onViewportActive:i,views:a,isPicking:o,preRenderStats:s={}}){let{device:c}=this.context;if(o)return;let l=t.filter(({props:{visible:e,collisionEnabled:t}})=>e&&t);if(l.length===0){this.channels={};return}let u=e?.filter(e=>e.useInPicking&&s[e.id]),d=s[`mask-effect`]?.didRender,f=this._groupByCollisionGroup(c,l),p=r[0],m=!this.lastViewport||!this.lastViewport.equals(p)||d;for(let e in f){let t=this.collisionFBOs[e],r=f[e],[o,s]=c.canvasContext.getPixelSize();t.resize({width:o/z,height:s/z}),this._render(r,{effects:u,layerFilter:n,onViewportActive:i,views:a,viewport:p,viewportChanged:m})}}_render(e,{effects:n,layerFilter:r,onViewportActive:i,views:a,viewport:o,viewportChanged:s}){let{collisionGroup:l}=e,u=this.channels[l];if(!u)return;let d=s||e===u||!c(u.layers,e.layers,1)||e.layerBounds.some((e,n)=>!t(e,u.layerBounds[n]))||e.allLayersLoaded!==u.allLayersLoaded||e.layers.some(e=>e.props.transitions);if(this.channels[l]=e,d){this.lastViewport=o;let t=this.collisionFBOs[l];this.collisionFilterPass.renderCollisionMap(t,{pass:`collision-filter`,isPicking:!0,layers:e.layers,effects:n,layerFilter:r,viewports:o?[o]:[],onViewportActive:i,views:a,moduleParameters:{dummyCollisionMap:this.dummyCollisionMap,devicePixelRatio:t.device.canvasContext.getDevicePixelRatio()/z}})}}_groupByCollisionGroup(e,t){let n={};for(let e of t){let{collisionGroup:t}=e.props,r=n[t];r||(r={collisionGroup:t,layers:[],layerBounds:[],allLayersLoaded:!0},n[t]=r),r.layers.push(e),r.layerBounds.push(e.getBounds()),e.isLoaded||(r.allLayersLoaded=!1)}for(let t of Object.keys(n))this.collisionFBOs[t]||this.createFBO(e,t),this.channels[t]||(this.channels[t]=n[t]);for(let e of Object.keys(this.collisionFBOs))n[e]||this.destroyFBO(e);return n}getModuleParameters(e){let{collisionGroup:t}=e.props,{collisionFBOs:n,dummyCollisionMap:r}=this;return{collisionFBO:n[t],dummyCollisionMap:r}}cleanup(){this.dummyCollisionMap&&=(this.dummyCollisionMap.delete(),void 0),this.channels={};for(let e of Object.keys(this.collisionFBOs))this.destroyFBO(e);this.collisionFBOs={},this.lastViewport=void 0}createFBO(e,t){let{width:n,height:r}=e.gl.canvas,i=e.createTexture({format:`rgba8unorm`,width:n,height:r,sampler:{minFilter:`nearest`,magFilter:`nearest`,addressModeU:`clamp-to-edge`,addressModeV:`clamp-to-edge`}}),a=e.createTexture({format:`depth16unorm`,width:n,height:r,mipmaps:!1,dataFormat:6402,type:5125});this.collisionFBOs[t]=e.createFramebuffer({id:`collision-${t}`,width:n,height:r,colorAttachments:[i],depthStencilAttachment:a})}destroyFBO(e){let t=this.collisionFBOs[e];t.colorAttachments[0]?.destroy(),t.depthStencilAttachment?.destroy(),t.destroy(),delete this.collisionFBOs[e]}},Ae={getCollisionPriority:{type:`accessor`,value:0},collisionEnabled:!0,collisionGroup:{type:`string`,value:`default`},collisionTestProps:{}},B=class extends d{getShaders(){return{modules:[De]}}draw({uniforms:e,context:t,moduleParameters:n}){let{collisionEnabled:r}=this.props,{collisionFBO:i,drawToCollisionMap:a}=n;e.collision_enabled=r&&!!i,a&&(this.props=this.clone(this.props.collisionTestProps).props)}initializeState(e,t){this.getAttributeManager()!==null&&(this.context.deck?._addDefaultEffect(new ke),this.getAttributeManager().add({collisionPriorities:{size:1,stepMode:`dynamic`,accessor:`getCollisionPriority`}}))}getNeedsPickingBuffer(){return this.props.collisionEnabled}};B.defaultProps=Ae,B.extensionName=`CollisionFilterExtension`;var je={name:`mask`,dependencies:[h],vs:`
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
`},getUniforms:e=>e&&`maskMap`in e?{mask_texture:e.maskMap}:{}},Me={blendColorOperation:`subtract`,blendColorSrcFactor:`zero`,blendColorDstFactor:`one`,blendAlphaOperation:`subtract`,blendAlphaSrcFactor:`zero`,blendAlphaDstFactor:`one`},Ne=class extends o{constructor(e,t){super(e,t);let{mapSize:n=2048}=t;this.maskMap=e.createTexture({format:`rgba8unorm`,width:n,height:n,sampler:{minFilter:`linear`,magFilter:`linear`,addressModeU:`clamp-to-edge`,addressModeV:`clamp-to-edge`}}),this.fbo=e.createFramebuffer({id:`maskmap`,width:n,height:n,colorAttachments:[this.maskMap]})}render(e){let t=2**e.channel,n=[255,255,255,255];super.render({...e,clearColor:n,colorMask:t,target:this.fbo,pass:`mask`})}getLayerParameters(e,t,n){return{...e.props.parameters,blend:!0,depthTest:!1,...Me}}shouldDrawLayer(e){return e.props.operation.includes(`mask`)}delete(){this.fbo.delete(),this.maskMap.delete()}};function V(e,t){let n=[1/0,1/0,-1/0,-1/0];for(let r of e){let e=r.getBounds();if(e){let i=r.projectPosition(e[0],{viewport:t,autoOffset:!1}),a=r.projectPosition(e[1],{viewport:t,autoOffset:!1});n[0]=Math.min(n[0],i[0]),n[1]=Math.min(n[1],i[1]),n[2]=Math.max(n[2],a[0]),n[3]=Math.max(n[3],a[1])}}return Number.isFinite(n[0])?n:null}var Pe=2048;function H(e){let{bounds:t,viewport:n,border:r=0}=e,{isGeospatial:i}=n;if(t[2]<=t[0]||t[3]<=t[1])return null;let a=n.unprojectPosition([(t[0]+t[2])/2,(t[1]+t[3])/2,0]),{width:o,height:c,zoom:l}=e;if(l===void 0){o-=r*2,c-=r*2;let e=Math.min(o/(t[2]-t[0]),c/(t[3]-t[1]));l=Math.min(Math.log2(e),20)}else if(!o||!c){let e=2**l;o=Math.round(Math.abs(t[2]-t[0])*e),c=Math.round(Math.abs(t[3]-t[1])*e);let n=Pe-r*2;if(o>n||c>n){let e=n/Math.max(o,c);o=Math.round(o*e),c=Math.round(c*e),l+=Math.log2(e)}}return i?new u({id:n.id,x:r,y:r,width:o,height:c,longitude:a[0],latitude:a[1],zoom:l,orthographic:!0}):new s({id:n.id,x:r,y:r,width:o,height:c,target:a,zoom:l,flipY:!1})}function Fe(e,t){let n;if(t&&t.length===2){let[r,i]=t,a=e.getBounds({z:r}),o=e.getBounds({z:i});n=[Math.min(a[0],o[0]),Math.min(a[1],o[1]),Math.max(a[2],o[2]),Math.max(a[3],o[3])]}else n=e.getBounds();let r=e.projectPosition(n.slice(0,2)),i=e.projectPosition(n.slice(2,4));return[r[0],r[1],i[0],i[1]]}function U(e,t,n){if(!e)return[0,0,1,1];let r=Ie(Fe(t,n));return e[2]-e[0]<=r[2]-r[0]&&e[3]-e[1]<=r[3]-r[1]?e:[Math.max(e[0],r[0]),Math.max(e[1],r[1]),Math.min(e[2],r[2]),Math.min(e[3],r[3])]}function Ie(e){let t=e[2]-e[0],n=e[3]-e[1],r=(e[0]+e[2])/2,i=(e[1]+e[3])/2;return[r-t,i-n,r+t,i+n]}var Le=class{constructor(){this.id=`mask-effect`,this.props=null,this.useInPicking=!0,this.order=0,this.channels=[],this.masks=null}setup({device:e}){this.dummyMaskMap=e.createTexture({width:1,height:1}),this.maskPass=new Ne(e,{id:`default-mask`}),this.maskMap=this.maskPass.maskMap}preRender({layers:t,layerFilter:n,viewports:r,onViewportActive:i,views:a,isPicking:o}){let s=!1;if(o)return{didRender:s};let c=t.filter(e=>e.props.visible&&e.props.operation.includes(`mask`));if(c.length===0)return this.masks=null,this.channels.length=0,{didRender:s};this.masks={};let l=this._sortMaskChannels(c),u=r[0],d=!this.lastViewport||!this.lastViewport.equals(u);if(u.resolution!==void 0)return e.warn(`MaskExtension is not supported in GlobeView`)(),{didRender:s};for(let e in l){let t=this._renderChannel(l[e],{layerFilter:n,onViewportActive:i,views:a,viewport:u,viewportChanged:d});s||=t}return{didRender:s}}_renderChannel(e,{layerFilter:n,onViewportActive:r,views:i,viewport:a,viewportChanged:o}){let s=!1,c=this.channels[e.index];if(!c)return s;let l=e===c||e.layers.length!==c.layers.length||e.layers.some((e,t)=>e!==c.layers[t]||e.props.transitions)||e.layerBounds.some((e,t)=>e!==c.layerBounds[t]);if(e.bounds=c.bounds,e.maskBounds=c.maskBounds,this.channels[e.index]=e,l||o){this.lastViewport=a;let o=V(e.layers,a);if(e.bounds=o&&U(o,a),l||!t(e.bounds,c.bounds)){let{maskPass:t,maskMap:c}=this,l=o&&H({bounds:e.bounds,viewport:a,width:c.width,height:c.height,border:1});e.maskBounds=l?l.getBounds():[0,0,1,1],t.render({pass:`mask`,channel:e.index,layers:e.layers,layerFilter:n,viewports:l?[l]:[],onViewportActive:r,views:i,moduleParameters:{devicePixelRatio:1}}),s=!0}}return this.masks[e.id]={index:e.index,bounds:e.maskBounds,coordinateOrigin:e.coordinateOrigin,coordinateSystem:e.coordinateSystem},s}_sortMaskChannels(t){let n={},r=0;for(let i of t){let{id:t}=i.root,a=n[t];if(!a){if(++r>4){e.warn(`Too many mask layers. The max supported is 4`)();continue}a={id:t,index:this.channels.findIndex(e=>e?.id===t),layers:[],layerBounds:[],coordinateOrigin:i.root.props.coordinateOrigin,coordinateSystem:i.root.props.coordinateSystem},n[t]=a}a.layers.push(i),a.layerBounds.push(i.getBounds())}for(let e=0;e<4;e++){let t=this.channels[e];(!t||!(t.id in n))&&(this.channels[e]=null)}for(let e in n){let t=n[e];t.index<0&&(t.index=this.channels.findIndex(e=>!e),this.channels[t.index]=t)}return n}getModuleParameters(){return{maskMap:this.masks?this.maskMap:this.dummyMaskMap,maskChannels:this.masks}}cleanup(){this.dummyMaskMap&&=(this.dummyMaskMap.delete(),void 0),this.maskPass&&(this.maskPass.delete(),this.maskPass=void 0,this.maskMap=void 0),this.lastViewport=void 0,this.masks=null,this.channels.length=0}},Re={maskId:``,maskByInstance:void 0,maskInverted:!1},W=class extends d{initializeState(){this.context.deck?._addDefaultEffect(new Le)}getShaders(){let e=`instancePositions`in this.getAttributeManager().attributes;return this.props.maskByInstance!==void 0&&(e=!!this.props.maskByInstance),this.state.maskByInstance=e,{modules:[je]}}draw({uniforms:t,context:n,moduleParameters:r}){t.mask_maskByInstance=this.state.maskByInstance;let{maskId:i,maskInverted:a}=this.props,{maskChannels:o}=r,{viewport:s}=n;if(o&&o[i]){let{index:e,bounds:n,coordinateOrigin:r}=o[i],{coordinateSystem:c}=o[i];t.mask_enabled=!0,t.mask_channel=e,t.mask_inverted=a,c===m.DEFAULT&&(c=s.isGeospatial?m.LNGLAT:m.CARTESIAN);let l={modelMatrix:null,fromCoordinateOrigin:r,fromCoordinateSystem:c},u=this.projectPosition([n[0],n[1],0],l),d=this.projectPosition([n[2],n[3],0],l);t.mask_bounds=[u[0],u[1],d[0],d[1]]}else i&&e.warn(`Could not find a mask layer with id: ${i}`)(),t.mask_enabled=!1}};W.defaultProps=Re,W.extensionName=`MaskExtension`;var G={NONE:0,WRITE_HEIGHT_MAP:1,USE_HEIGHT_MAP:2,USE_COVER:3,USE_COVER_ONLY:4,SKIP:5},K=Object.keys(G).map(e=>`const float TERRAIN_MODE_${e} = ${G[e]}.0;`).join(`
`),q={name:`terrain`,dependencies:[h],inject:{"vs:#decl":`
uniform float terrain_mode;
uniform sampler2D terrain_map;
uniform vec4 terrain_bounds;
out vec3 commonPos;
`+K,"vs:#main-start":`
if (terrain_mode == TERRAIN_MODE_SKIP) {
gl_Position = vec4(0.0);
return;
}
`,"vs:DECKGL_FILTER_GL_POSITION":`
commonPos = geometry.position.xyz;
if (terrain_mode == TERRAIN_MODE_WRITE_HEIGHT_MAP) {
vec2 texCoords = (commonPos.xy - terrain_bounds.xy) / terrain_bounds.zw;
position = vec4(texCoords * 2.0 - 1.0, 0.0, 1.0);
commonPos.z += project_uCommonOrigin.z;
}
if (terrain_mode == TERRAIN_MODE_USE_HEIGHT_MAP) {
vec3 anchor = geometry.worldPosition;
anchor.z = 0.0;
vec3 anchorCommon = project_position(anchor);
vec2 texCoords = (anchorCommon.xy - terrain_bounds.xy) / terrain_bounds.zw;
if (texCoords.x >= 0.0 && texCoords.y >= 0.0 && texCoords.x <= 1.0 && texCoords.y <= 1.0) {
float terrainZ = texture(terrain_map, texCoords).r;
geometry.position.z += terrainZ;
position = project_common_position_to_clipspace(geometry.position);
}
}
`,"fs:#decl":`
uniform float terrain_mode;
uniform sampler2D terrain_map;
uniform vec4 terrain_bounds;
in vec3 commonPos;
`+K,"fs:#main-start":`
if (terrain_mode == TERRAIN_MODE_WRITE_HEIGHT_MAP) {
fragColor = vec4(commonPos.z, 0.0, 0.0, 1.0);
return;
}
`,"fs:DECKGL_FILTER_COLOR":`
if ((terrain_mode == TERRAIN_MODE_USE_COVER) || (terrain_mode == TERRAIN_MODE_USE_COVER_ONLY)) {
vec2 texCoords = (commonPos.xy - terrain_bounds.xy) / terrain_bounds.zw;
vec4 pixel = texture(terrain_map, texCoords);
if (terrain_mode == TERRAIN_MODE_USE_COVER_ONLY) {
color = pixel;
} else {
color = pixel + color * (1.0 - pixel.a);
}
return;
}
`},getUniforms:(e={},t)=>{if(`dummyHeightMap`in e){let{drawToTerrainHeightMap:n,heightMap:r,heightMapBounds:i,dummyHeightMap:a,terrainCover:o,useTerrainHeightMap:s,terrainSkipRender:c}=e,{project_uCommonOrigin:l}=t,u=c?G.SKIP:G.NONE,d=a,f=null;if(n)u=G.WRITE_HEIGHT_MAP,f=i;else if(s&&r)u=G.USE_HEIGHT_MAP,d=r,f=i;else if(o){let t=e.picking?.isActive;d=(t?o.getPickingFramebuffer():o.getRenderFramebuffer())?.colorAttachments[0].texture,t&&(u=G.SKIP),d?(u=u===G.SKIP?G.USE_COVER_ONLY:G.USE_COVER,f=o.bounds):d=a}return{terrain_mode:u,terrain_map:d,terrain_bounds:f?[f[0]-l[0],f[1]-l[1],f[2]-f[0],f[3]-f[1]]:[0,0,0,0]}}return null}};function J(e,t){return e.createFramebuffer({id:t.id,colorAttachments:[e.createTexture({id:t.id,...t.float&&{format:`rgba32float`,type:5126},mipmaps:!1,sampler:t.interpolate===!1?{minFilter:`nearest`,magFilter:`nearest`}:{minFilter:`linear`,magFilter:`linear`}})]})}var ze=class{constructor(e){this.isDirty=!0,this.renderViewport=null,this.bounds=null,this.layers=[],this.targetBounds=null,this.targetBoundsCommon=null,this.targetLayer=e,this.tile=Y(e)}get id(){return this.targetLayer.id}get isActive(){return!!this.targetLayer.getCurrentLayer()}shouldUpdate({targetLayer:e,viewport:t,layers:n,layerNeedsRedraw:r}){e&&(this.targetLayer=e);let i=t?this._updateViewport(t):!1,a=n?this._updateLayers(n):!1;if(r){for(let e of this.layers)if(r[e]){a=!0;break}}return a||i}_updateLayers(e){let t=!1;if(e=this.tile?Be(this.tile,e):e,e.length!==this.layers.length)t=!0;else for(let n=0;n<e.length;n++)if(e[n].id!==this.layers[n]){t=!0;break}return t&&(this.layers=e.map(e=>e.id)),t}_updateViewport(e){let t=this.targetLayer,n=!1;if(this.tile&&`boundingBox`in this.tile){if(!this.targetBounds){n=!0,this.targetBounds=this.tile.boundingBox;let t=e.projectPosition(this.targetBounds[0]),r=e.projectPosition(this.targetBounds[1]);this.targetBoundsCommon=[t[0],t[1],r[0],r[1]]}}else this.targetBounds!==t.getBounds()&&(n=!0,this.targetBounds=t.getBounds(),this.targetBoundsCommon=V([t],e));if(!this.targetBoundsCommon)return!1;let r=Math.ceil(e.zoom+.5);if(this.tile)this.bounds=this.targetBoundsCommon;else{let t=this.renderViewport?.zoom;n||=r!==t;let i=U(this.targetBoundsCommon,e),a=this.bounds;n=n||!a||i.some((e,t)=>e!==a[t]),this.bounds=i}return n&&(this.renderViewport=H({bounds:this.bounds,zoom:r,viewport:e})),n}getRenderFramebuffer(){return!this.renderViewport||this.layers.length===0?null:(this.fbo||=J(this.targetLayer.context.device,{id:this.id}),this.fbo)}getPickingFramebuffer(){return!this.renderViewport||this.layers.length===0&&!this.targetLayer.props.pickable?null:(this.pickingFbo||=J(this.targetLayer.context.device,{id:`${this.id}-picking`,interpolate:!1}),this.pickingFbo)}filterLayers(e){return e.filter(({id:e})=>this.layers.includes(e))}delete(){let{fbo:e,pickingFbo:t}=this;e&&(e.colorAttachments[0].destroy(),e.destroy()),t&&(t.colorAttachments[0].destroy(),t.destroy())}};function Be(e,t){return t.filter(t=>{let n=Y(t);return n?X(e.boundingBox,n.boundingBox):!0})}function Y(e){for(;e;){let{tile:t}=e.props;if(t)return t;e=e.parent}return null}function X(e,t){return e&&t?e[0][0]<t[1][0]&&t[0][0]<e[1][0]&&e[0][1]<t[1][1]&&t[0][1]<e[1][1]:!1}var Ve={blendColorOperation:`max`,blendColorSrcFactor:`one`,blendColorDstFactor:`one`,blendAlphaOperation:`max`,blendAlphaSrcFactor:`one`,blendAlphaDstFactor:`one`},He=class extends o{getRenderableLayers(e,t){let{layers:n}=t,r=[],i=this._getDrawLayerParams(e,t,!0);for(let e=0;e<n.length;e++){let t=n[e];!t.isComposite&&i[e].shouldDrawLayer&&r.push(t)}return r}renderHeightMap(e,t){let n=e.getRenderFramebuffer(),r=e.renderViewport;!n||!r||(n.resize(r),this.render({...t,target:n,pass:`terrain-height-map`,layers:t.layers,viewports:[r],effects:[],clearColor:[0,0,0,0]}))}renderTerrainCover(e,t){let n=e.getRenderFramebuffer(),r=e.renderViewport;if(!n||!r)return;let i=e.filterLayers(t.layers);n.resize(r),this.render({...t,target:n,pass:`terrain-cover-${e.id}`,layers:i,effects:[],viewports:[r],clearColor:[0,0,0,0]})}getLayerParameters(e,t,n){return{...e.props.parameters,blend:!0,depthTest:!1,...e.props.operation.includes(`terrain`)&&Ve}}},Ue=class extends p{constructor(){super(...arguments),this.drawParameters={}}getRenderableLayers(e,t){let{layers:n}=t,r=[];this.drawParameters={},this._resetColorEncoder(t.pickZ);let i=this._getDrawLayerParams(e,t);for(let e=0;e<n.length;e++){let t=n[e];!t.isComposite&&i[e].shouldDrawLayer&&(r.push(t),this.drawParameters[t.id]=i[e].layerParameters)}return r}renderTerrainCover(e,t){let n=e.getPickingFramebuffer(),r=e.renderViewport;if(!n||!r)return;let i=e.filterLayers(t.layers),a=e.targetLayer;a.props.pickable&&i.unshift(a),n.resize(r),this.render({...t,pickingFBO:n,pass:`terrain-cover-picking-${e.id}`,layers:i,effects:[],viewports:[r],cullRect:void 0,deviceRect:r,pickZ:!1})}getLayerParameters(e,t,n){let r;return this.drawParameters[e.id]?r=this.drawParameters[e.id]:(r=super.getLayerParameters(e,t,n),r.blend=!0),{...r,depthTest:!1}}},Z=2048,Q=class{static isSupported(e){return e.isTextureFormatRenderable(`rgba32float`)}constructor(e){this.renderViewport=null,this.bounds=null,this.layers=[],this.layersBounds=[],this.layersBoundsCommon=null,this.lastViewport=null,this.device=e}getRenderFramebuffer(){return this.renderViewport?(this.fbo||=J(this.device,{id:`height-map`,float:!0}),this.fbo):null}shouldUpdate({layers:e,viewport:t}){let n=e.length!==this.layers.length||e.some((e,t)=>e!==this.layers[t]||e.props.transitions||e.getBounds()!==this.layersBounds[t]);n&&(this.layers=e,this.layersBounds=e.map(e=>e.getBounds()),this.layersBoundsCommon=V(e,t));let r=!this.lastViewport||!t.equals(this.lastViewport);if(!this.layersBoundsCommon)this.renderViewport=null;else if(n||r){let e=U(this.layersBoundsCommon,t);if(e[2]<=e[0]||e[3]<=e[1])return this.renderViewport=null,!1;this.bounds=e,this.lastViewport=t;let n=t.scale,r=(e[2]-e[0])*n,i=(e[3]-e[1])*n;return this.renderViewport=r>0||i>0?H({bounds:[t.center[0]-1,t.center[1]-1,t.center[0]+1,t.center[1]+1],zoom:t.zoom,width:Math.min(r,Z),height:Math.min(i,Z),viewport:t}):null,!0}return!1}delete(){this.fbo&&(this.fbo.colorAttachments[0].delete(),this.fbo.delete())}},We=class{constructor(){this.id=`terrain-effect`,this.props=null,this.useInPicking=!0,this.isPicking=!1,this.isDrapingEnabled=!1,this.terrainCovers=new Map}setup({device:t,deck:n}){this.dummyHeightMap=t.createTexture({width:1,height:1,data:new Uint8Array([0,0,0,0])}),this.terrainPass=new He(t,{id:`terrain`}),this.terrainPickingPass=new Ue(t,{id:`terrain-picking`}),Q.isSupported(t)?this.heightMap=new Q(t):e.warn(`Terrain offset mode is not supported by this browser`)(),n._addDefaultShaderModule(q)}preRender(e){if(e.pickZ){this.isDrapingEnabled=!1;return}let{viewports:t}=e,n=e.pass.startsWith(`picking`);this.isPicking=n,this.isDrapingEnabled=!0;let r=t[0],i=(n?this.terrainPickingPass:this.terrainPass).getRenderableLayers(r,e),a=i.filter(e=>e.props.operation.includes(`terrain`));if(a.length===0)return;n||i.filter(e=>e.state.terrainDrawMode===`offset`).length>0&&this._updateHeightMap(a,r,e);let o=i.filter(e=>e.state.terrainDrawMode===`drape`);this._updateTerrainCovers(a,o,r,e)}getModuleParameters(e){let{terrainDrawMode:t}=e.state;return{heightMap:this.heightMap?.getRenderFramebuffer()?.colorAttachments[0].texture||null,heightMapBounds:this.heightMap?.bounds,dummyHeightMap:this.dummyHeightMap,terrainCover:this.isDrapingEnabled?this.terrainCovers.get(e.id):null,useTerrainHeightMap:t===`offset`,terrainSkipRender:t===`drape`||!e.props.operation.includes(`draw`)}}cleanup({deck:e}){this.dummyHeightMap&&=(this.dummyHeightMap.delete(),void 0),this.heightMap&&=(this.heightMap.delete(),void 0);for(let e of this.terrainCovers.values())e.delete();this.terrainCovers.clear(),e._removeDefaultShaderModule(q)}_updateHeightMap(e,t,n){this.heightMap&&this.heightMap.shouldUpdate({layers:e,viewport:t})&&this.terrainPass.renderHeightMap(this.heightMap,{...n,layers:e,moduleParameters:{heightMapBounds:this.heightMap.bounds,dummyHeightMap:this.dummyHeightMap,devicePixelRatio:1,drawToTerrainHeightMap:!0}})}_updateTerrainCovers(e,t,n,r){let i={};for(let e of t)e.state.terrainCoverNeedsRedraw&&(i[e.id]=!0,e.state.terrainCoverNeedsRedraw=!1);for(let e of this.terrainCovers.values())e.isDirty=e.isDirty||e.shouldUpdate({layerNeedsRedraw:i});for(let i of e)this._updateTerrainCover(i,t,n,r);this.isPicking||this._pruneTerrainCovers()}_updateTerrainCover(e,t,n,r){let i=this.isPicking?this.terrainPickingPass:this.terrainPass,a=this.terrainCovers.get(e.id);a||(a=new ze(e),this.terrainCovers.set(e.id,a));try{let o=a.shouldUpdate({targetLayer:e,viewport:n,layers:t});(this.isPicking||a.isDirty||o)&&(i.renderTerrainCover(a,{...r,layers:t,moduleParameters:{dummyHeightMap:this.dummyHeightMap,terrainSkipRender:!1,devicePixelRatio:1}}),this.isPicking||(a.isDirty=!1))}catch(t){e.raiseError(t,`Error rendering terrain cover ${a.id}`)}}_pruneTerrainCovers(){let e=[];for(let[t,n]of this.terrainCovers)n.isActive||e.push(t);for(let t of e)this.terrainCovers.delete(t)}},Ge={terrainDrawMode:void 0},$=class extends d{getShaders(){return{modules:[q]}}initializeState(){this.context.deck?._addDefaultEffect(new We)}updateState(e){let{props:t,oldProps:n}=e;if(this.state.terrainDrawMode&&t.terrainDrawMode===n.terrainDrawMode&&t.extruded===n.extruded)return;let{terrainDrawMode:r}=t;if(!r){let e=this.props.extruded,t=this.getAttributeManager()?.attributes,n=t&&`instancePositions`in t;r=e||n?`offset`:`drape`}this.setState({terrainDrawMode:r})}onNeedsRedraw(){let e=this.state;e.terrainDrawMode===`drape`&&(e.terrainCoverNeedsRedraw=!0)}};$.defaultProps=Ge,$.extensionName=`TerrainExtension`;export{_ as BrushingExtension,R as ClipExtension,B as CollisionFilterExtension,w as DataFilterExtension,I as FillStyleExtension,O as Fp64Extension,W as MaskExtension,M as PathStyleExtension,$ as _TerrainExtension,T as project64};