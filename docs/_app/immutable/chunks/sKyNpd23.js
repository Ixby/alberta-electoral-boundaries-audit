import{it as e,nt as t}from"./pPhJVxZQ.js";import{A as n,C as r,D as i,S as a,_ as o,a as s,c,d as l,f as u,g as d,j as f,k as p,n as m,o as h,v as g,w as _,x as v}from"./9dJrIGTn.js";var y=class extends l{constructor(e={}){let{id:t=p(`cube-geometry`),indices:n=!0}=e;super(n?{...e,id:t,topology:`triangle-list`,indices:{size:1,value:b},attributes:{...D,...e.attributes}}:{...e,id:t,topology:`triangle-list`,indices:void 0,attributes:{...O,...e.attributes}})}},b=new Uint16Array([0,1,2,0,2,3,4,5,6,4,6,7,8,9,10,8,10,11,12,13,14,12,14,15,16,17,18,16,18,19,20,21,22,20,22,23]),x=new Float32Array([-1,-1,1,1,-1,1,1,1,1,-1,1,1,-1,-1,-1,-1,1,-1,1,1,-1,1,-1,-1,-1,1,-1,-1,1,1,1,1,1,1,1,-1,-1,-1,-1,1,-1,-1,1,-1,1,-1,-1,1,1,-1,-1,1,1,-1,1,1,1,1,-1,1,-1,-1,-1,-1,-1,1,-1,1,1,-1,1,-1]),S=new Float32Array([0,0,1,0,0,1,0,0,1,0,0,1,0,0,-1,0,0,-1,0,0,-1,0,0,-1,0,1,0,0,1,0,0,1,0,0,1,0,0,-1,0,0,-1,0,0,-1,0,0,-1,0,1,0,0,1,0,0,1,0,0,1,0,0,-1,0,0,-1,0,0,-1,0,0,-1,0,0]),C=new Float32Array([0,0,1,0,1,1,0,1,1,0,1,1,0,1,0,0,0,1,0,0,1,0,1,1,1,1,0,1,0,0,1,0,1,0,1,1,0,1,0,0,0,0,1,0,1,1,0,1]),w=new Float32Array([1,-1,1,-1,-1,1,-1,-1,-1,1,-1,-1,1,-1,1,-1,-1,-1,1,1,1,1,-1,1,1,-1,-1,1,1,-1,1,1,1,1,-1,-1,-1,1,1,1,1,1,1,1,-1,-1,1,-1,-1,1,1,1,1,-1,-1,-1,1,-1,1,1,-1,1,-1,-1,-1,-1,-1,-1,1,-1,1,-1,1,1,1,-1,1,1,-1,-1,1,-1,-1,1,1,-1,1,1,1,1,1,-1,-1,-1,-1,-1,-1,1,-1,1,1,-1,1,-1,-1,-1,1,-1]),T=new Float32Array([1,1,0,1,0,0,1,0,1,1,0,0,1,1,0,1,0,0,1,0,1,1,0,0,1,1,0,1,0,0,1,0,1,1,0,0,1,1,0,1,0,0,1,0,1,1,0,0,1,1,0,1,0,0,0,0,1,0,1,1,1,1,0,1,0,0,1,0,1,1,0,0]),E=new Float32Array([1,0,1,1,0,0,1,1,0,0,0,1,1,0,0,1,1,0,1,1,0,0,0,1,1,1,1,1,1,0,1,1,1,0,0,1,1,1,0,1,1,1,1,1,1,0,0,1,0,1,1,1,1,1,1,1,1,1,0,1,0,1,0,1,0,1,1,1,1,1,0,1,0,0,1,1,0,1,1,1,0,1,0,1,0,0,0,1,0,0,1,1,0,1,0,1,1,1,1,1,0,1,1,1,0,0,1,1,0,0,1,1,1,0,1,1,1,1,1,1,1,0,0,1,0,0,0,1,0,1,0,1,1,1,0,1,1,0,0,1,0,1,0,1]),D={POSITION:{size:3,value:x},NORMAL:{size:3,value:S},TEXCOORD_0:{size:2,value:C}},O={POSITION:{size:3,value:w},TEXCOORD_0:{size:2,value:T},COLOR_0:{size:3,value:E}},k=`#version 300 es
#define SHADER_NAME arc-layer-vertex-shader
in vec3 positions;
in vec4 instanceSourceColors;
in vec4 instanceTargetColors;
in vec3 instanceSourcePositions;
in vec3 instanceSourcePositions64Low;
in vec3 instanceTargetPositions;
in vec3 instanceTargetPositions64Low;
in vec3 instancePickingColors;
in float instanceWidths;
in float instanceHeights;
in float instanceTilts;
uniform bool greatCircle;
uniform bool useShortestPath;
uniform float numSegments;
uniform float opacity;
uniform float widthScale;
uniform float widthMinPixels;
uniform float widthMaxPixels;
uniform int widthUnits;
out vec4 vColor;
out vec2 uv;
out float isValid;
float paraboloid(float distance, float sourceZ, float targetZ, float ratio) {
float deltaZ = targetZ - sourceZ;
float dh = distance * instanceHeights;
if (dh == 0.0) {
return sourceZ + deltaZ * ratio;
}
float unitZ = deltaZ / dh;
float p2 = unitZ * unitZ + 1.0;
float dir = step(deltaZ, 0.0);
float z0 = mix(sourceZ, targetZ, dir);
float r = mix(ratio, 1.0 - ratio, dir);
return sqrt(r * (p2 - r)) * dh + z0;
}
vec2 getExtrusionOffset(vec2 line_clipspace, float offset_direction, float width) {
vec2 dir_screenspace = normalize(line_clipspace * project_uViewportSize);
dir_screenspace = vec2(-dir_screenspace.y, dir_screenspace.x);
return dir_screenspace * offset_direction * width / 2.0;
}
float getSegmentRatio(float index) {
return smoothstep(0.0, 1.0, index / (numSegments - 1.0));
}
vec3 interpolateFlat(vec3 source, vec3 target, float segmentRatio) {
float distance = length(source.xy - target.xy);
float z = paraboloid(distance, source.z, target.z, segmentRatio);
float tiltAngle = radians(instanceTilts);
vec2 tiltDirection = normalize(target.xy - source.xy);
vec2 tilt = vec2(-tiltDirection.y, tiltDirection.x) * z * sin(tiltAngle);
return vec3(
mix(source.xy, target.xy, segmentRatio) + tilt,
z * cos(tiltAngle)
);
}
float getAngularDist (vec2 source, vec2 target) {
vec2 sourceRadians = radians(source);
vec2 targetRadians = radians(target);
vec2 sin_half_delta = sin((sourceRadians - targetRadians) / 2.0);
vec2 shd_sq = sin_half_delta * sin_half_delta;
float a = shd_sq.y + cos(sourceRadians.y) * cos(targetRadians.y) * shd_sq.x;
return 2.0 * asin(sqrt(a));
}
vec3 interpolateGreatCircle(vec3 source, vec3 target, vec3 source3D, vec3 target3D, float angularDist, float t) {
vec2 lngLat;
if(abs(angularDist - PI) < 0.001) {
lngLat = (1.0 - t) * source.xy + t * target.xy;
} else {
float a = sin((1.0 - t) * angularDist);
float b = sin(t * angularDist);
vec3 p = source3D.yxz * a + target3D.yxz * b;
lngLat = degrees(vec2(atan(p.y, -p.x), atan(p.z, length(p.xy))));
}
float z = paraboloid(angularDist * EARTH_RADIUS, source.z, target.z, t);
return vec3(lngLat, z);
}
void main(void) {
geometry.worldPosition = instanceSourcePositions;
geometry.worldPositionAlt = instanceTargetPositions;
float segmentIndex = positions.x;
float segmentRatio = getSegmentRatio(segmentIndex);
float prevSegmentRatio = getSegmentRatio(max(0.0, segmentIndex - 1.0));
float nextSegmentRatio = getSegmentRatio(min(numSegments - 1.0, segmentIndex + 1.0));
float indexDir = mix(-1.0, 1.0, step(segmentIndex, 0.0));
isValid = 1.0;
uv = vec2(segmentRatio, positions.y);
geometry.uv = uv;
geometry.pickingColor = instancePickingColors;
vec4 curr;
vec4 next;
vec3 source;
vec3 target;
if ((greatCircle || project_uProjectionMode == PROJECTION_MODE_GLOBE) && project_uCoordinateSystem == COORDINATE_SYSTEM_LNGLAT) {
source = project_globe_(vec3(instanceSourcePositions.xy, 0.0));
target = project_globe_(vec3(instanceTargetPositions.xy, 0.0));
float angularDist = getAngularDist(instanceSourcePositions.xy, instanceTargetPositions.xy);
vec3 prevPos = interpolateGreatCircle(instanceSourcePositions, instanceTargetPositions, source, target, angularDist, prevSegmentRatio);
vec3 currPos = interpolateGreatCircle(instanceSourcePositions, instanceTargetPositions, source, target, angularDist, segmentRatio);
vec3 nextPos = interpolateGreatCircle(instanceSourcePositions, instanceTargetPositions, source, target, angularDist, nextSegmentRatio);
if (abs(currPos.x - prevPos.x) > 180.0) {
indexDir = -1.0;
isValid = 0.0;
} else if (abs(currPos.x - nextPos.x) > 180.0) {
indexDir = 1.0;
isValid = 0.0;
}
nextPos = indexDir < 0.0 ? prevPos : nextPos;
nextSegmentRatio = indexDir < 0.0 ? prevSegmentRatio : nextSegmentRatio;
if (isValid == 0.0) {
nextPos.x += nextPos.x > 0.0 ? -360.0 : 360.0;
float t = ((currPos.x > 0.0 ? 180.0 : -180.0) - currPos.x) / (nextPos.x - currPos.x);
currPos = mix(currPos, nextPos, t);
segmentRatio = mix(segmentRatio, nextSegmentRatio, t);
}
vec3 currPos64Low = mix(instanceSourcePositions64Low, instanceTargetPositions64Low, segmentRatio);
vec3 nextPos64Low = mix(instanceSourcePositions64Low, instanceTargetPositions64Low, nextSegmentRatio);
curr = project_position_to_clipspace(currPos, currPos64Low, vec3(0.0), geometry.position);
next = project_position_to_clipspace(nextPos, nextPos64Low, vec3(0.0));
} else {
vec3 source_world = instanceSourcePositions;
vec3 target_world = instanceTargetPositions;
if (useShortestPath) {
source_world.x = mod(source_world.x + 180., 360.0) - 180.;
target_world.x = mod(target_world.x + 180., 360.0) - 180.;
float deltaLng = target_world.x - source_world.x;
if (deltaLng > 180.) target_world.x -= 360.;
if (deltaLng < -180.) source_world.x -= 360.;
}
source = project_position(source_world, instanceSourcePositions64Low);
target = project_position(target_world, instanceTargetPositions64Low);
float antiMeridianX = 0.0;
if (useShortestPath) {
if (project_uProjectionMode == PROJECTION_MODE_WEB_MERCATOR_AUTO_OFFSET) {
antiMeridianX = -(project_uCoordinateOrigin.x + 180.) / 360. * TILE_SIZE;
}
float thresholdRatio = (antiMeridianX - source.x) / (target.x - source.x);
if (prevSegmentRatio <= thresholdRatio && nextSegmentRatio > thresholdRatio) {
isValid = 0.0;
indexDir = sign(segmentRatio - thresholdRatio);
segmentRatio = thresholdRatio;
}
}
nextSegmentRatio = indexDir < 0.0 ? prevSegmentRatio : nextSegmentRatio;
vec3 currPos = interpolateFlat(source, target, segmentRatio);
vec3 nextPos = interpolateFlat(source, target, nextSegmentRatio);
if (useShortestPath) {
if (nextPos.x < antiMeridianX) {
currPos.x += TILE_SIZE;
nextPos.x += TILE_SIZE;
}
}
curr = project_common_position_to_clipspace(vec4(currPos, 1.0));
next = project_common_position_to_clipspace(vec4(nextPos, 1.0));
geometry.position = vec4(currPos, 1.0);
}
float widthPixels = clamp(
project_size_to_pixel(instanceWidths * widthScale, widthUnits),
widthMinPixels, widthMaxPixels
);
vec3 offset = vec3(
getExtrusionOffset((next.xy - curr.xy) * indexDir, positions.y, widthPixels),
0.0);
DECKGL_FILTER_SIZE(offset, geometry);
DECKGL_FILTER_GL_POSITION(curr, geometry);
gl_Position = curr + vec4(project_pixel_size_to_clipspace(offset.xy), 0.0, 0.0);
vec4 color = mix(instanceSourceColors, instanceTargetColors, segmentRatio);
vColor = vec4(color.rgb, color.a * opacity);
DECKGL_FILTER_COLOR(vColor, geometry);
}
`,A=`#version 300 es
#define SHADER_NAME arc-layer-fragment-shader
precision highp float;
in vec4 vColor;
in vec2 uv;
in float isValid;
out vec4 fragColor;
void main(void) {
if (isValid == 0.0) {
discard;
}
fragColor = vColor;
geometry.uv = uv;
DECKGL_FILTER_COLOR(fragColor, geometry);
}
`,j=[0,0,0,255],M={getSourcePosition:{type:`accessor`,value:e=>e.sourcePosition},getTargetPosition:{type:`accessor`,value:e=>e.targetPosition},getSourceColor:{type:`accessor`,value:j},getTargetColor:{type:`accessor`,value:j},getWidth:{type:`accessor`,value:1},getHeight:{type:`accessor`,value:1},getTilt:{type:`accessor`,value:0},greatCircle:!1,numSegments:{type:`number`,value:50,min:1},widthUnits:`pixels`,widthScale:{type:`number`,value:1,min:0},widthMinPixels:{type:`number`,value:0,min:0},widthMaxPixels:{type:`number`,value:2**53-1,min:0}},N=class extends h{getBounds(){return this.getAttributeManager()?.getBounds([`instanceSourcePositions`,`instanceTargetPositions`])}getShaders(){return super.getShaders({vs:k,fs:A,modules:[g,d]})}get wrapLongitude(){return!1}initializeState(){this.getAttributeManager().addInstanced({instanceSourcePositions:{size:3,type:`float64`,fp64:this.use64bitPositions(),transition:!0,accessor:`getSourcePosition`},instanceTargetPositions:{size:3,type:`float64`,fp64:this.use64bitPositions(),transition:!0,accessor:`getTargetPosition`},instanceSourceColors:{size:this.props.colorFormat.length,type:`unorm8`,transition:!0,accessor:`getSourceColor`,defaultValue:j},instanceTargetColors:{size:this.props.colorFormat.length,type:`unorm8`,transition:!0,accessor:`getTargetColor`,defaultValue:j},instanceWidths:{size:1,transition:!0,accessor:`getWidth`,defaultValue:1},instanceHeights:{size:1,transition:!0,accessor:`getHeight`,defaultValue:1},instanceTilts:{size:1,transition:!0,accessor:`getTilt`,defaultValue:0}})}updateState(e){super.updateState(e);let{props:t,oldProps:n,changeFlags:r}=e;(r.extensionsChanged||t.numSegments!==n.numSegments)&&(this.state.model?.destroy(),this.state.model=this._getModel(),this.getAttributeManager().invalidateAll())}draw({uniforms:e}){let{widthUnits:t,widthScale:n,widthMinPixels:r,widthMaxPixels:i,greatCircle:o,wrapLongitude:s}=this.props,c=this.state.model;c.setUniforms(e),c.setUniforms({greatCircle:o,widthUnits:a[t],widthScale:n,widthMinPixels:r,widthMaxPixels:i,useShortestPath:s}),c.draw(this.context.renderPass)}_getModel(){let{numSegments:e}=this.props,t=[];for(let n=0;n<e;n++)t=t.concat([n,1,0,n,-1,0]);let n=new u(this.context.device,{...this.getShaders(),id:this.props.id,bufferLayout:this.getAttributeManager().getBufferLayouts(),geometry:new l({topology:`triangle-strip`,attributes:{positions:{size:3,value:new Float32Array(t)}}}),isInstanced:!0});return n.setUniforms({numSegments:e}),n}};N.layerName=`ArcLayer`,N.defaultProps=M;var ee=new Uint32Array([0,2,1,0,3,2]),te=new Float32Array([0,1,0,0,1,0,1,1]);function ne(e,t){if(!t)return re(e);let n=Math.max(Math.abs(e[0][0]-e[3][0]),Math.abs(e[1][0]-e[2][0])),r=Math.max(Math.abs(e[1][1]-e[0][1]),Math.abs(e[2][1]-e[3][1])),i=Math.ceil(n/t)+1,a=Math.ceil(r/t)+1,o=(i-1)*(a-1)*6,s=new Uint32Array(o),c=new Float32Array(i*a*2),l=new Float64Array(i*a*3),u=0,d=0;for(let t=0;t<i;t++){let n=t/(i-1);for(let r=0;r<a;r++){let i=r/(a-1),o=ie(e,n,i);l[u*3+0]=o[0],l[u*3+1]=o[1],l[u*3+2]=o[2]||0,c[u*2+0]=n,c[u*2+1]=1-i,t>0&&r>0&&(s[d++]=u-a,s[d++]=u-a-1,s[d++]=u-1,s[d++]=u-a,s[d++]=u-1,s[d++]=u),u++}}return{vertexCount:o,positions:l,indices:s,texCoords:c}}function re(e){let t=new Float64Array(12);for(let n=0;n<e.length;n++)t[n*3+0]=e[n][0],t[n*3+1]=e[n][1],t[n*3+2]=e[n][2]||0;return{vertexCount:6,positions:t,indices:ee,texCoords:te}}function ie(e,t,n){return i(i(e[0],e[1],n),i(e[3],e[2],n),t)}var ae=`#version 300 es
#define SHADER_NAME bitmap-layer-vertex-shader

in vec2 texCoords;
in vec3 positions;
in vec3 positions64Low;

out vec2 vTexCoord;
out vec2 vTexPos;

uniform float coordinateConversion;

const vec3 pickingColor = vec3(1.0, 0.0, 0.0);

void main(void) {
  geometry.worldPosition = positions;
  geometry.uv = texCoords;
  geometry.pickingColor = pickingColor;

  gl_Position = project_position_to_clipspace(positions, positions64Low, vec3(0.0), geometry.position);
  DECKGL_FILTER_GL_POSITION(gl_Position, geometry);

  vTexCoord = texCoords;

  if (coordinateConversion < -0.5) {
    vTexPos = geometry.position.xy + project_uCommonOrigin.xy;
  } else if (coordinateConversion > 0.5) {
    vTexPos = geometry.worldPosition.xy;
  }

  vec4 color = vec4(0.0);
  DECKGL_FILTER_COLOR(color, geometry);
}
`,oe=`#version 300 es
#define SHADER_NAME bitmap-layer-fragment-shader

#ifdef GL_ES
precision highp float;
#endif

uniform sampler2D bitmapTexture;

in vec2 vTexCoord;
in vec2 vTexPos;

out vec4 fragColor;

uniform float desaturate;
uniform vec4 transparentColor;
uniform vec3 tintColor;
uniform float opacity;

uniform float coordinateConversion;
uniform vec4 bounds;

/* projection utils */
const float TILE_SIZE = 512.0;
const float PI = 3.1415926536;
const float WORLD_SCALE = TILE_SIZE / PI / 2.0;

// from degrees to Web Mercator
vec2 lnglat_to_mercator(vec2 lnglat) {
  float x = lnglat.x;
  float y = clamp(lnglat.y, -89.9, 89.9);
  return vec2(
    radians(x) + PI,
    PI + log(tan(PI * 0.25 + radians(y) * 0.5))
  ) * WORLD_SCALE;
}

// from Web Mercator to degrees
vec2 mercator_to_lnglat(vec2 xy) {
  xy /= WORLD_SCALE;
  return degrees(vec2(
    xy.x - PI,
    atan(exp(xy.y - PI)) * 2.0 - PI * 0.5
  ));
}
/* End projection utils */

// apply desaturation
vec3 color_desaturate(vec3 color) {
  float luminance = (color.r + color.g + color.b) * 0.333333333;
  return mix(color, vec3(luminance), desaturate);
}

// apply tint
vec3 color_tint(vec3 color) {
  return color * tintColor;
}

// blend with background color
vec4 apply_opacity(vec3 color, float alpha) {
  if (transparentColor.a == 0.0) {
    return vec4(color, alpha);
  }
  float blendedAlpha = alpha + transparentColor.a * (1.0 - alpha);
  float highLightRatio = alpha / blendedAlpha;
  vec3 blendedRGB = mix(transparentColor.rgb, color, highLightRatio);
  return vec4(blendedRGB, blendedAlpha);
}

vec2 getUV(vec2 pos) {
  return vec2(
    (pos.x - bounds[0]) / (bounds[2] - bounds[0]),
    (pos.y - bounds[3]) / (bounds[1] - bounds[3])
  );
}


vec3 packUVsIntoRGB(vec2 uv) {
  // Extract the top 8 bits. We want values to be truncated down so we can add a fraction
  vec2 uv8bit = floor(uv * 256.);

  // Calculate the normalized remainders of u and v parts that do not fit into 8 bits
  // Scale and clamp to 0-1 range
  vec2 uvFraction = fract(uv * 256.);
  vec2 uvFraction4bit = floor(uvFraction * 16.);

  // Remainder can be encoded in blue channel, encode as 4 bits for pixel coordinates
  float fractions = uvFraction4bit.x + uvFraction4bit.y * 16.;

  return vec3(uv8bit, fractions) / 255.;
}


void main(void) {
  vec2 uv = vTexCoord;
  if (coordinateConversion < -0.5) {
    vec2 lnglat = mercator_to_lnglat(vTexPos);
    uv = getUV(lnglat);
  } else if (coordinateConversion > 0.5) {
    vec2 commonPos = lnglat_to_mercator(vTexPos);
    uv = getUV(commonPos);
  }
  vec4 bitmapColor = texture(bitmapTexture, uv);

  fragColor = apply_opacity(color_tint(color_desaturate(bitmapColor.rgb)), bitmapColor.a * opacity);

  geometry.uv = uv;
  DECKGL_FILTER_COLOR(fragColor, geometry);

  if (bool(picking.isActive) && !bool(picking.isAttribute)) {
    // Since instance information is not used, we can use picking color for pixel index
    fragColor.rgb = packUVsIntoRGB(uv);
  }
}
`,se={image:{type:`image`,value:null,async:!0},bounds:{type:`array`,value:[1,0,0,1],compare:!0},_imageCoordinateSystem:v.DEFAULT,desaturate:{type:`number`,min:0,max:1,value:0},transparentColor:{type:`color`,value:[0,0,0,0]},tintColor:{type:`color`,value:[255,255,255]},textureParameters:{type:`object`,ignore:!0,value:null}},ce=class extends h{getShaders(){return super.getShaders({vs:ae,fs:oe,modules:[g,d]})}initializeState(){let e=this.getAttributeManager();e.remove([`instancePickingColors`]),e.add({indices:{size:1,isIndexed:!0,update:e=>e.value=this.state.mesh.indices,noAlloc:!0},positions:{size:3,type:`float64`,fp64:this.use64bitPositions(),update:e=>e.value=this.state.mesh.positions,noAlloc:!0},texCoords:{size:2,update:e=>e.value=this.state.mesh.texCoords,noAlloc:!0}})}updateState({props:e,oldProps:t,changeFlags:n}){let r=this.getAttributeManager();if(n.extensionsChanged&&(this.state.model?.destroy(),this.state.model=this._getModel(),r.invalidateAll()),e.bounds!==t.bounds){let e=this.state.mesh,t=this._createMesh();this.state.model.setVertexCount(t.vertexCount);for(let n in t)e&&e[n]!==t[n]&&r.invalidate(n);this.setState({mesh:t,...this._getCoordinateUniforms()})}else e._imageCoordinateSystem!==t._imageCoordinateSystem&&this.setState(this._getCoordinateUniforms())}getPickingInfo(e){let{image:t}=this.props,n=e.info;if(!n.color||!t)return n.bitmap=null,n;let{width:r,height:i}=t;n.index=0;let a=le(n.color);return n.bitmap={size:{width:r,height:i},uv:a,pixel:[Math.floor(a[0]*r),Math.floor(a[1]*i)]},n}disablePickingIndex(){this.setState({disablePicking:!0})}restorePickingColors(){this.setState({disablePicking:!1})}_updateAutoHighlight(e){super._updateAutoHighlight({...e,color:this.encodePickingColor(0)})}_createMesh(){let{bounds:e}=this.props,t=e;return ue(e)&&(t=[[e[0],e[1]],[e[0],e[3]],[e[2],e[3]],[e[2],e[1]]]),ne(t,this.context.viewport.resolution)}_getModel(){return new u(this.context.device,{...this.getShaders(),id:this.props.id,bufferLayout:this.getAttributeManager().getBufferLayouts(),topology:`triangle-list`,isInstanced:!1})}draw(e){let{uniforms:t,moduleParameters:n}=e,{model:r,coordinateConversion:i,bounds:a,disablePicking:o}=this.state,{image:s,desaturate:c,transparentColor:l,tintColor:u}=this.props;n.picking.isActive&&o||s&&r&&(r.setUniforms(t),r.setBindings({bitmapTexture:s}),r.setUniforms({desaturate:c,transparentColor:l.map(e=>e/255),tintColor:u.slice(0,3).map(e=>e/255),coordinateConversion:i,bounds:a}),r.draw(this.context.renderPass))}_getCoordinateUniforms(){let{LNGLAT:e,CARTESIAN:t,DEFAULT:n}=v,{_imageCoordinateSystem:r}=this.props;if(r!==n){let{bounds:n}=this.props;if(!ue(n))throw Error(`_imageCoordinateSystem only supports rectangular bounds`);let i=this.context.viewport.resolution?e:t;if(r=r===e?e:t,r===e&&i===t)return{coordinateConversion:-1,bounds:n};if(r===t&&i===e){let e=o([n[0],n[1]]),t=o([n[2],n[3]]);return{coordinateConversion:1,bounds:[e[0],e[1],t[0],t[1]]}}}return{coordinateConversion:0,bounds:[0,0,0,0]}}};ce.layerName=`BitmapLayer`,ce.defaultProps=se;function le(e){let[t,n,r]=e,i=(r&240)/256;return[(t+(r&15)/16)/256,(n+i)/256]}function ue(e){return Number.isFinite(e[0])}var de=`#version 300 es
#define SHADER_NAME icon-layer-vertex-shader
in vec2 positions;
in vec3 instancePositions;
in vec3 instancePositions64Low;
in float instanceSizes;
in float instanceAngles;
in vec4 instanceColors;
in vec3 instancePickingColors;
in vec4 instanceIconFrames;
in float instanceColorModes;
in vec2 instanceOffsets;
in vec2 instancePixelOffset;
uniform float sizeScale;
uniform vec2 iconsTextureDim;
uniform float sizeMinPixels;
uniform float sizeMaxPixels;
uniform bool billboard;
uniform int sizeUnits;
out float vColorMode;
out vec4 vColor;
out vec2 vTextureCoords;
out vec2 uv;
vec2 rotate_by_angle(vec2 vertex, float angle) {
float angle_radian = angle * PI / 180.0;
float cos_angle = cos(angle_radian);
float sin_angle = sin(angle_radian);
mat2 rotationMatrix = mat2(cos_angle, -sin_angle, sin_angle, cos_angle);
return rotationMatrix * vertex;
}
void main(void) {
geometry.worldPosition = instancePositions;
geometry.uv = positions;
geometry.pickingColor = instancePickingColors;
uv = positions;
vec2 iconSize = instanceIconFrames.zw;
float sizePixels = clamp(
project_size_to_pixel(instanceSizes * sizeScale, sizeUnits),
sizeMinPixels, sizeMaxPixels
);
float instanceScale = iconSize.y == 0.0 ? 0.0 : sizePixels / iconSize.y;
vec2 pixelOffset = positions / 2.0 * iconSize + instanceOffsets;
pixelOffset = rotate_by_angle(pixelOffset, instanceAngles) * instanceScale;
pixelOffset += instancePixelOffset;
pixelOffset.y *= -1.0;
if (billboard)  {
gl_Position = project_position_to_clipspace(instancePositions, instancePositions64Low, vec3(0.0), geometry.position);
DECKGL_FILTER_GL_POSITION(gl_Position, geometry);
vec3 offset = vec3(pixelOffset, 0.0);
DECKGL_FILTER_SIZE(offset, geometry);
gl_Position.xy += project_pixel_size_to_clipspace(offset.xy);
} else {
vec3 offset_common = vec3(project_pixel_size(pixelOffset), 0.0);
DECKGL_FILTER_SIZE(offset_common, geometry);
gl_Position = project_position_to_clipspace(instancePositions, instancePositions64Low, offset_common, geometry.position);
DECKGL_FILTER_GL_POSITION(gl_Position, geometry);
}
vTextureCoords = mix(
instanceIconFrames.xy,
instanceIconFrames.xy + iconSize,
(positions.xy + 1.0) / 2.0
) / iconsTextureDim;
vColor = instanceColors;
DECKGL_FILTER_COLOR(vColor, geometry);
vColorMode = instanceColorModes;
}
`,fe=`#version 300 es
#define SHADER_NAME icon-layer-fragment-shader
precision highp float;
uniform float opacity;
uniform sampler2D iconsTexture;
uniform float alphaCutoff;
in float vColorMode;
in vec4 vColor;
in vec2 vTextureCoords;
in vec2 uv;
out vec4 fragColor;
void main(void) {
geometry.uv = uv;
vec4 texColor = texture(iconsTexture, vTextureCoords);
vec3 color = mix(texColor.rgb, vColor.rgb, vColorMode);
float a = texColor.a * opacity * vColor.a;
if (a < alphaCutoff) {
discard;
}
fragColor = vec4(color, a);
DECKGL_FILTER_COLOR(fragColor, geometry);
}
`,pe=1024,me=4,he=()=>{},ge={minFilter:`linear`,mipmapFilter:`linear`,magFilter:`linear`,addressModeU:`clamp-to-edge`,addressModeV:`clamp-to-edge`},_e={x:0,y:0,width:0,height:0};function ve(e){return 2**Math.ceil(Math.log2(e))}function ye(e,t,n,r){let i=Math.min(n/t.width,r/t.height),a=Math.floor(t.width*i),o=Math.floor(t.height*i);return i===1?{data:t,width:a,height:o}:(e.canvas.height=o,e.canvas.width=a,e.clearRect(0,0,a,o),e.drawImage(t,0,0,t.width,t.height,0,0,a,o),{data:e.canvas,width:a,height:o})}function P(e){return e&&(e.id||e.url)}function be(e,t,n,r){let{width:i,height:a,device:o}=e,s=o.createTexture({format:`rgba8unorm`,width:t,height:n,sampler:r}),c=o.createCommandEncoder();return c.copyTextureToTexture({source:e,destination:s,width:i,height:a}),c.finish(),e.destroy(),s}function xe(e,t,n){for(let r=0;r<t.length;r++){let{icon:i,xOffset:a}=t[r],o=P(i);e[o]={...i,x:a,y:n}}}function Se({icons:e,buffer:t,mapping:n={},xOffset:r=0,yOffset:i=0,rowHeight:a=0,canvasWidth:o}){let s=[];for(let c=0;c<e.length;c++){let l=e[c];if(!n[P(l)]){let{height:e,width:c}=l;r+c+t>o&&(xe(n,s,i),r=0,i=a+i+t,a=0,s=[]),s.push({icon:l,xOffset:r}),r=r+c+t,a=Math.max(a,e)}}return s.length>0&&xe(n,s,i),{mapping:n,rowHeight:a,xOffset:r,yOffset:i,canvasWidth:o,canvasHeight:ve(a+i+t)}}function Ce(e,t,n){if(!e||!t)return null;n||={};let r={},{iterable:i,objectInfo:a}=c(e);for(let e of i){a.index++;let i=t(e,a),o=P(i);if(!i)throw Error(`Icon is missing.`);if(!i.url)throw Error(`Icon url is missing.`);!r[o]&&(!n[o]||i.url!==n[o].url)&&(r[o]={...i,source:e,sourceIndex:a.index})}return r}var we=class{constructor(e,{onUpdate:t=he,onError:n=he}){this._loadOptions=null,this._texture=null,this._externalTexture=null,this._mapping={},this._textureParameters=null,this._pendingCount=0,this._autoPacking=!1,this._xOffset=0,this._yOffset=0,this._rowHeight=0,this._buffer=me,this._canvasWidth=pe,this._canvasHeight=0,this._canvas=null,this.device=e,this.onUpdate=t,this.onError=n}finalize(){this._texture?.delete()}getTexture(){return this._texture||this._externalTexture}getIconMapping(e){let t=this._autoPacking?P(e):e;return this._mapping[t]||_e}setProps({loadOptions:e,autoPacking:t,iconAtlas:n,iconMapping:r,textureParameters:i}){e&&(this._loadOptions=e),t!==void 0&&(this._autoPacking=t),r&&(this._mapping=r),n&&(this._texture?.delete(),this._texture=null,this._externalTexture=n),i&&(this._textureParameters=i)}get isLoaded(){return this._pendingCount===0}packIcons(e,t){if(!this._autoPacking||typeof document>`u`)return;let n=Object.values(Ce(e,t,this._mapping)||{});if(n.length>0){let{mapping:e,xOffset:t,yOffset:r,rowHeight:i,canvasHeight:a}=Se({icons:n,buffer:this._buffer,canvasWidth:this._canvasWidth,mapping:this._mapping,rowHeight:this._rowHeight,xOffset:this._xOffset,yOffset:this._yOffset});this._rowHeight=i,this._mapping=e,this._xOffset=t,this._yOffset=r,this._canvasHeight=a,this._texture||=this.device.createTexture({format:`rgba8unorm`,width:this._canvasWidth,height:this._canvasHeight,sampler:this._textureParameters||ge}),this._texture.height!==this._canvasHeight&&(this._texture=be(this._texture,this._canvasWidth,this._canvasHeight,this._textureParameters||ge)),this.onUpdate(),this._canvas=this._canvas||document.createElement(`canvas`),this._loadIcons(n)}}_loadIcons(e){let t=this._canvas.getContext(`2d`,{willReadFrequently:!0});for(let n of e)this._pendingCount++,f(n.url,this._loadOptions).then(e=>{let r=P(n),i=this._mapping[r],{x:a,y:o,width:s,height:c}=i,{data:l,width:u,height:d}=ye(t,e,s,c);this._texture.setSubImageData({data:l,x:a+(s-u)/2,y:o+(c-d)/2,width:u,height:d}),i.width=u,i.height=d,this._texture.generateMipmap(),this.onUpdate()}).catch(e=>{this.onError({url:n.url,source:n.source,sourceIndex:n.sourceIndex,loadOptions:this._loadOptions,error:e})}).finally(()=>{this._pendingCount--})}},Te=[0,0,0,255],Ee={iconAtlas:{type:`image`,value:null,async:!0},iconMapping:{type:`object`,value:{},async:!0},sizeScale:{type:`number`,value:1,min:0},billboard:!0,sizeUnits:`pixels`,sizeMinPixels:{type:`number`,min:0,value:0},sizeMaxPixels:{type:`number`,min:0,value:2**53-1},alphaCutoff:{type:`number`,value:.05,min:0,max:1},getPosition:{type:`accessor`,value:e=>e.position},getIcon:{type:`accessor`,value:e=>e.icon},getColor:{type:`accessor`,value:Te},getSize:{type:`accessor`,value:1},getAngle:{type:`accessor`,value:0},getPixelOffset:{type:`accessor`,value:[0,0]},onIconError:{type:`function`,value:null,optional:!0},textureParameters:{type:`object`,ignore:!0,value:null}},F=class extends h{getShaders(){return super.getShaders({vs:de,fs:fe,modules:[g,d]})}initializeState(){this.state={iconManager:new we(this.context.device,{onUpdate:this._onUpdate.bind(this),onError:this._onError.bind(this)})},this.getAttributeManager().addInstanced({instancePositions:{size:3,type:`float64`,fp64:this.use64bitPositions(),transition:!0,accessor:`getPosition`},instanceSizes:{size:1,transition:!0,accessor:`getSize`,defaultValue:1},instanceOffsets:{size:2,accessor:`getIcon`,transform:this.getInstanceOffset},instanceIconFrames:{size:4,accessor:`getIcon`,transform:this.getInstanceIconFrame},instanceColorModes:{size:1,type:`uint8`,accessor:`getIcon`,transform:this.getInstanceColorMode},instanceColors:{size:this.props.colorFormat.length,type:`unorm8`,transition:!0,accessor:`getColor`,defaultValue:Te},instanceAngles:{size:1,transition:!0,accessor:`getAngle`},instancePixelOffset:{size:2,transition:!0,accessor:`getPixelOffset`}})}updateState(e){super.updateState(e);let{props:t,oldProps:n,changeFlags:r}=e,i=this.getAttributeManager(),{iconAtlas:a,iconMapping:o,data:s,getIcon:c,textureParameters:l}=t,{iconManager:u}=this.state;if(typeof a==`string`)return;let d=a||this.internalState.isAsyncPropLoading(`iconAtlas`);u.setProps({loadOptions:t.loadOptions,autoPacking:!d,iconAtlas:a,iconMapping:d?o:null,textureParameters:l}),d?n.iconMapping!==t.iconMapping&&i.invalidate(`getIcon`):(r.dataChanged||r.updateTriggersChanged&&(r.updateTriggersChanged.all||r.updateTriggersChanged.getIcon))&&u.packIcons(s,c),r.extensionsChanged&&(this.state.model?.destroy(),this.state.model=this._getModel(),i.invalidateAll())}get isLoaded(){return super.isLoaded&&this.state.iconManager.isLoaded}finalizeState(e){super.finalizeState(e),this.state.iconManager.finalize()}draw({uniforms:e}){let{sizeScale:t,sizeMinPixels:n,sizeMaxPixels:r,sizeUnits:i,billboard:o,alphaCutoff:s}=this.props,{iconManager:c}=this.state,l=c.getTexture();if(l){let c=this.state.model;c.setBindings({iconsTexture:l}),c.setUniforms(e),c.setUniforms({iconsTextureDim:[l.width,l.height],sizeUnits:a[i],sizeScale:t,sizeMinPixels:n,sizeMaxPixels:r,billboard:o,alphaCutoff:s}),c.draw(this.context.renderPass)}}_getModel(){let e=[-1,-1,1,-1,-1,1,1,1];return new u(this.context.device,{...this.getShaders(),id:this.props.id,bufferLayout:this.getAttributeManager().getBufferLayouts(),geometry:new l({topology:`triangle-strip`,attributes:{positions:{size:2,value:new Float32Array(e)}}}),isInstanced:!0})}_onUpdate(){this.setNeedsRedraw()}_onError(e){let t=this.getCurrentLayer()?.props.onIconError;t?t(e):n.error(e.error.message)()}getInstanceOffset(e){let{width:t,height:n,anchorX:r=t/2,anchorY:i=n/2}=this.state.iconManager.getIconMapping(e);return[t/2-r,n/2-i]}getInstanceColorMode(e){return+!!this.state.iconManager.getIconMapping(e).mask}getInstanceIconFrame(e){let{x:t,y:n,width:r,height:i}=this.state.iconManager.getIconMapping(e);return[t,n,r,i]}};F.defaultProps=Ee,F.layerName=`IconLayer`;var De=`#version 300 es
#define SHADER_NAME line-layer-vertex-shader
in vec3 positions;
in vec3 instanceSourcePositions;
in vec3 instanceTargetPositions;
in vec3 instanceSourcePositions64Low;
in vec3 instanceTargetPositions64Low;
in vec4 instanceColors;
in vec3 instancePickingColors;
in float instanceWidths;
uniform float opacity;
uniform float widthScale;
uniform float widthMinPixels;
uniform float widthMaxPixels;
uniform float useShortestPath;
uniform int widthUnits;
out vec4 vColor;
out vec2 uv;
vec2 getExtrusionOffset(vec2 line_clipspace, float offset_direction, float width) {
vec2 dir_screenspace = normalize(line_clipspace * project_uViewportSize);
dir_screenspace = vec2(-dir_screenspace.y, dir_screenspace.x);
return dir_screenspace * offset_direction * width / 2.0;
}
vec3 splitLine(vec3 a, vec3 b, float x) {
float t = (x - a.x) / (b.x - a.x);
return vec3(x, mix(a.yz, b.yz, t));
}
void main(void) {
geometry.worldPosition = instanceSourcePositions;
geometry.worldPositionAlt = instanceTargetPositions;
vec3 source_world = instanceSourcePositions;
vec3 target_world = instanceTargetPositions;
vec3 source_world_64low = instanceSourcePositions64Low;
vec3 target_world_64low = instanceTargetPositions64Low;
if (useShortestPath > 0.5 || useShortestPath < -0.5) {
source_world.x = mod(source_world.x + 180., 360.0) - 180.;
target_world.x = mod(target_world.x + 180., 360.0) - 180.;
float deltaLng = target_world.x - source_world.x;
if (deltaLng * useShortestPath > 180.) {
source_world.x += 360. * useShortestPath;
source_world = splitLine(source_world, target_world, 180. * useShortestPath);
source_world_64low = vec3(0.0);
} else if (deltaLng * useShortestPath < -180.) {
target_world.x += 360. * useShortestPath;
target_world = splitLine(source_world, target_world, 180. * useShortestPath);
target_world_64low = vec3(0.0);
} else if (useShortestPath < 0.) {
gl_Position = vec4(0.);
return;
}
}
vec4 source_commonspace;
vec4 target_commonspace;
vec4 source = project_position_to_clipspace(source_world, source_world_64low, vec3(0.), source_commonspace);
vec4 target = project_position_to_clipspace(target_world, target_world_64low, vec3(0.), target_commonspace);
float segmentIndex = positions.x;
vec4 p = mix(source, target, segmentIndex);
geometry.position = mix(source_commonspace, target_commonspace, segmentIndex);
uv = positions.xy;
geometry.uv = uv;
geometry.pickingColor = instancePickingColors;
float widthPixels = clamp(
project_size_to_pixel(instanceWidths * widthScale, widthUnits),
widthMinPixels, widthMaxPixels
);
vec3 offset = vec3(
getExtrusionOffset(target.xy - source.xy, positions.y, widthPixels),
0.0);
DECKGL_FILTER_SIZE(offset, geometry);
DECKGL_FILTER_GL_POSITION(p, geometry);
gl_Position = p + vec4(project_pixel_size_to_clipspace(offset.xy), 0.0, 0.0);
vColor = vec4(instanceColors.rgb, instanceColors.a * opacity);
DECKGL_FILTER_COLOR(vColor, geometry);
}
`,Oe=`#version 300 es
#define SHADER_NAME line-layer-fragment-shader
precision highp float;
in vec4 vColor;
in vec2 uv;
out vec4 fragColor;
void main(void) {
geometry.uv = uv;
fragColor = vColor;
DECKGL_FILTER_COLOR(fragColor, geometry);
}
`,ke={getSourcePosition:{type:`accessor`,value:e=>e.sourcePosition},getTargetPosition:{type:`accessor`,value:e=>e.targetPosition},getColor:{type:`accessor`,value:[0,0,0,255]},getWidth:{type:`accessor`,value:1},widthUnits:`pixels`,widthScale:{type:`number`,value:1,min:0},widthMinPixels:{type:`number`,value:0,min:0},widthMaxPixels:{type:`number`,value:2**53-1,min:0}},Ae=class extends h{getBounds(){return this.getAttributeManager()?.getBounds([`instanceSourcePositions`,`instanceTargetPositions`])}getShaders(){return super.getShaders({vs:De,fs:Oe,modules:[g,d]})}get wrapLongitude(){return!1}initializeState(){this.getAttributeManager().addInstanced({instanceSourcePositions:{size:3,type:`float64`,fp64:this.use64bitPositions(),transition:!0,accessor:`getSourcePosition`},instanceTargetPositions:{size:3,type:`float64`,fp64:this.use64bitPositions(),transition:!0,accessor:`getTargetPosition`},instanceColors:{size:this.props.colorFormat.length,type:`unorm8`,transition:!0,accessor:`getColor`,defaultValue:[0,0,0,255]},instanceWidths:{size:1,transition:!0,accessor:`getWidth`,defaultValue:1}})}updateState(e){super.updateState(e),e.changeFlags.extensionsChanged&&(this.state.model?.destroy(),this.state.model=this._getModel(),this.getAttributeManager().invalidateAll())}draw({uniforms:e}){let{widthUnits:t,widthScale:n,widthMinPixels:r,widthMaxPixels:i,wrapLongitude:o}=this.props,s=this.state.model;s.setUniforms(e),s.setUniforms({widthUnits:a[t],widthScale:n,widthMinPixels:r,widthMaxPixels:i,useShortestPath:+!!o}),s.draw(this.context.renderPass),o&&(s.setUniforms({useShortestPath:-1}),s.draw(this.context.renderPass))}_getModel(){let e=[0,-1,0,0,1,0,1,-1,0,1,1,0];return new u(this.context.device,{...this.getShaders(),id:this.props.id,bufferLayout:this.getAttributeManager().getBufferLayouts(),geometry:new l({topology:`triangle-strip`,attributes:{positions:{size:3,value:new Float32Array(e)}}}),isInstanced:!0})}};Ae.layerName=`LineLayer`,Ae.defaultProps=ke;var je=`#version 300 es
#define SHADER_NAME point-cloud-layer-vertex-shader
in vec3 positions;
in vec3 instanceNormals;
in vec4 instanceColors;
in vec3 instancePositions;
in vec3 instancePositions64Low;
in vec3 instancePickingColors;
uniform float opacity;
uniform float radiusPixels;
uniform int sizeUnits;
out vec4 vColor;
out vec2 unitPosition;
void main(void) {
geometry.worldPosition = instancePositions;
geometry.normal = project_normal(instanceNormals);
unitPosition = positions.xy;
geometry.uv = unitPosition;
geometry.pickingColor = instancePickingColors;
vec3 offset = vec3(positions.xy * project_size_to_pixel(radiusPixels, sizeUnits), 0.0);
DECKGL_FILTER_SIZE(offset, geometry);
gl_Position = project_position_to_clipspace(instancePositions, instancePositions64Low, vec3(0.), geometry.position);
DECKGL_FILTER_GL_POSITION(gl_Position, geometry);
gl_Position.xy += project_pixel_size_to_clipspace(offset.xy);
vec3 lightColor = lighting_getLightColor(instanceColors.rgb, project_uCameraPosition, geometry.position.xyz, geometry.normal);
vColor = vec4(lightColor, instanceColors.a * opacity);
DECKGL_FILTER_COLOR(vColor, geometry);
}
`,Me=`#version 300 es
#define SHADER_NAME point-cloud-layer-fragment-shader
precision highp float;
in vec4 vColor;
in vec2 unitPosition;
out vec4 fragColor;
void main(void) {
geometry.uv = unitPosition;
float distToCenter = length(unitPosition);
if (distToCenter > 1.0) {
discard;
}
fragColor = vColor;
DECKGL_FILTER_COLOR(fragColor, geometry);
}
`,Ne=[0,0,0,255],Pe=[0,0,1],Fe={sizeUnits:`pixels`,pointSize:{type:`number`,min:0,value:10},getPosition:{type:`accessor`,value:e=>e.position},getNormal:{type:`accessor`,value:Pe},getColor:{type:`accessor`,value:Ne},material:!0,radiusPixels:{deprecatedFor:`pointSize`}};function Ie(e){let{header:t,attributes:n}=e;if(!(!t||!n)&&(e.length=t.vertexCount,n.POSITION&&(n.instancePositions=n.POSITION),n.NORMAL&&(n.instanceNormals=n.NORMAL),n.COLOR_0)){let{size:e,value:t}=n.COLOR_0;n.instanceColors={size:e,type:`unorm8`,value:t}}}var Le=class extends h{getShaders(){return super.getShaders({vs:je,fs:Me,modules:[g,r,d]})}initializeState(){this.getAttributeManager().addInstanced({instancePositions:{size:3,type:`float64`,fp64:this.use64bitPositions(),transition:!0,accessor:`getPosition`},instanceNormals:{size:3,transition:!0,accessor:`getNormal`,defaultValue:Pe},instanceColors:{size:this.props.colorFormat.length,type:`unorm8`,transition:!0,accessor:`getColor`,defaultValue:Ne}})}updateState(e){let{changeFlags:t,props:n}=e;super.updateState(e),t.extensionsChanged&&(this.state.model?.destroy(),this.state.model=this._getModel(),this.getAttributeManager().invalidateAll()),t.dataChanged&&Ie(n.data)}draw({uniforms:e}){let{pointSize:t,sizeUnits:n}=this.props,r=this.state.model;r.setUniforms(e),r.setUniforms({sizeUnits:a[n],radiusPixels:t}),r.draw(this.context.renderPass)}_getModel(){let e=[];for(let t=0;t<3;t++){let n=t/3*Math.PI*2;e.push(Math.cos(n)*2,Math.sin(n)*2,0)}return new u(this.context.device,{...this.getShaders(),id:this.props.id,bufferLayout:this.getAttributeManager().getBufferLayouts(),geometry:new l({topology:`triangle-list`,attributes:{positions:new Float32Array(e)}}),isInstanced:!0})}};Le.layerName=`PointCloudLayer`,Le.defaultProps=Fe;var Re=`#version 300 es
#define SHADER_NAME scatterplot-layer-vertex-shader
in vec3 positions;
in vec3 instancePositions;
in vec3 instancePositions64Low;
in float instanceRadius;
in float instanceLineWidths;
in vec4 instanceFillColors;
in vec4 instanceLineColors;
in vec3 instancePickingColors;
uniform float opacity;
uniform float radiusScale;
uniform float radiusMinPixels;
uniform float radiusMaxPixels;
uniform float lineWidthScale;
uniform float lineWidthMinPixels;
uniform float lineWidthMaxPixels;
uniform float stroked;
uniform bool filled;
uniform bool antialiasing;
uniform bool billboard;
uniform int radiusUnits;
uniform int lineWidthUnits;
out vec4 vFillColor;
out vec4 vLineColor;
out vec2 unitPosition;
out float innerUnitRadius;
out float outerRadiusPixels;
void main(void) {
geometry.worldPosition = instancePositions;
outerRadiusPixels = clamp(
project_size_to_pixel(radiusScale * instanceRadius, radiusUnits),
radiusMinPixels, radiusMaxPixels
);
float lineWidthPixels = clamp(
project_size_to_pixel(lineWidthScale * instanceLineWidths, lineWidthUnits),
lineWidthMinPixels, lineWidthMaxPixels
);
outerRadiusPixels += stroked * lineWidthPixels / 2.0;
float edgePadding = antialiasing ? (outerRadiusPixels + SMOOTH_EDGE_RADIUS) / outerRadiusPixels : 1.0;
unitPosition = edgePadding * positions.xy;
geometry.uv = unitPosition;
geometry.pickingColor = instancePickingColors;
innerUnitRadius = 1.0 - stroked * lineWidthPixels / outerRadiusPixels;
if (billboard) {
gl_Position = project_position_to_clipspace(instancePositions, instancePositions64Low, vec3(0.0), geometry.position);
DECKGL_FILTER_GL_POSITION(gl_Position, geometry);
vec3 offset = edgePadding * positions * outerRadiusPixels;
DECKGL_FILTER_SIZE(offset, geometry);
gl_Position.xy += project_pixel_size_to_clipspace(offset.xy);
} else {
vec3 offset = edgePadding * positions * project_pixel_size(outerRadiusPixels);
DECKGL_FILTER_SIZE(offset, geometry);
gl_Position = project_position_to_clipspace(instancePositions, instancePositions64Low, offset, geometry.position);
DECKGL_FILTER_GL_POSITION(gl_Position, geometry);
}
vFillColor = vec4(instanceFillColors.rgb, instanceFillColors.a * opacity);
DECKGL_FILTER_COLOR(vFillColor, geometry);
vLineColor = vec4(instanceLineColors.rgb, instanceLineColors.a * opacity);
DECKGL_FILTER_COLOR(vLineColor, geometry);
}
`,ze=`#version 300 es
#define SHADER_NAME scatterplot-layer-fragment-shader
precision highp float;
uniform bool filled;
uniform float stroked;
uniform bool antialiasing;
in vec4 vFillColor;
in vec4 vLineColor;
in vec2 unitPosition;
in float innerUnitRadius;
in float outerRadiusPixels;
out vec4 fragColor;
void main(void) {
geometry.uv = unitPosition;
float distToCenter = length(unitPosition) * outerRadiusPixels;
float inCircle = antialiasing ?
smoothedge(distToCenter, outerRadiusPixels) :
step(distToCenter, outerRadiusPixels);
if (inCircle == 0.0) {
discard;
}
if (stroked > 0.5) {
float isLine = antialiasing ?
smoothedge(innerUnitRadius * outerRadiusPixels, distToCenter) :
step(innerUnitRadius * outerRadiusPixels, distToCenter);
if (filled) {
fragColor = mix(vFillColor, vLineColor, isLine);
} else {
if (isLine == 0.0) {
discard;
}
fragColor = vec4(vLineColor.rgb, vLineColor.a * isLine);
}
} else if (!filled) {
discard;
} else {
fragColor = vFillColor;
}
fragColor.a *= inCircle;
DECKGL_FILTER_COLOR(fragColor, geometry);
}
`,Be=[0,0,0,255],Ve={radiusUnits:`meters`,radiusScale:{type:`number`,min:0,value:1},radiusMinPixels:{type:`number`,min:0,value:0},radiusMaxPixels:{type:`number`,min:0,value:2**53-1},lineWidthUnits:`meters`,lineWidthScale:{type:`number`,min:0,value:1},lineWidthMinPixels:{type:`number`,min:0,value:0},lineWidthMaxPixels:{type:`number`,min:0,value:2**53-1},stroked:!1,filled:!0,billboard:!1,antialiasing:!0,getPosition:{type:`accessor`,value:e=>e.position},getRadius:{type:`accessor`,value:1},getFillColor:{type:`accessor`,value:Be},getLineColor:{type:`accessor`,value:Be},getLineWidth:{type:`accessor`,value:1},strokeWidth:{deprecatedFor:`getLineWidth`},outline:{deprecatedFor:`stroked`},getColor:{deprecatedFor:[`getFillColor`,`getLineColor`]}},He=class extends h{getShaders(){return super.getShaders({vs:Re,fs:ze,modules:[g,d]})}initializeState(){this.getAttributeManager().addInstanced({instancePositions:{size:3,type:`float64`,fp64:this.use64bitPositions(),transition:!0,accessor:`getPosition`},instanceRadius:{size:1,transition:!0,accessor:`getRadius`,defaultValue:1},instanceFillColors:{size:this.props.colorFormat.length,transition:!0,type:`unorm8`,accessor:`getFillColor`,defaultValue:[0,0,0,255]},instanceLineColors:{size:this.props.colorFormat.length,transition:!0,type:`unorm8`,accessor:`getLineColor`,defaultValue:[0,0,0,255]},instanceLineWidths:{size:1,transition:!0,accessor:`getLineWidth`,defaultValue:1}})}updateState(e){super.updateState(e),e.changeFlags.extensionsChanged&&(this.state.model?.destroy(),this.state.model=this._getModel(),this.getAttributeManager().invalidateAll())}draw({uniforms:e}){let{radiusUnits:t,radiusScale:n,radiusMinPixels:r,radiusMaxPixels:i,stroked:o,filled:s,billboard:c,antialiasing:l,lineWidthUnits:u,lineWidthScale:d,lineWidthMinPixels:f,lineWidthMaxPixels:p}=this.props,m=this.state.model;m.setUniforms(e),m.setUniforms({stroked:+!!o,filled:s,billboard:c,antialiasing:l,radiusUnits:a[t],radiusScale:n,radiusMinPixels:r,radiusMaxPixels:i,lineWidthUnits:a[u],lineWidthScale:d,lineWidthMinPixels:f,lineWidthMaxPixels:p}),m.draw(this.context.renderPass)}_getModel(){let e=[-1,-1,0,1,-1,0,-1,1,0,1,1,0];return new u(this.context.device,{...this.getShaders(),id:this.props.id,bufferLayout:this.getAttributeManager().getBufferLayouts(),geometry:new l({topology:`triangle-strip`,attributes:{positions:{size:3,value:new Float32Array(e)}}}),isInstanced:!0})}};He.defaultProps=Ve,He.layerName=`ScatterplotLayer`;var Ue={CLOCKWISE:1,COUNTER_CLOCKWISE:-1};function We(e,t,n={}){return Ge(e,n)===t?!1:(Je(e,n),!0)}function Ge(e,t={}){return Math.sign(qe(e,t))}var Ke={x:0,y:1,z:2};function qe(e,t={}){let{start:n=0,end:r=e.length,plane:i=`xy`}=t,a=t.size||2,o=0,s=Ke[i[0]],c=Ke[i[1]];for(let t=n,i=r-a;t<r;t+=a)o+=(e[t+s]-e[i+s])*(e[t+c]+e[i+c]),i=t;return o/2}function Je(e,t){let{start:n=0,end:r=e.length,size:i=2}=t,a=(r-n)/i,o=Math.floor(a/2);for(let t=0;t<o;++t){let r=n+t*i,o=n+(a-1-t)*i;for(let t=0;t<i;++t){let n=e[r+t];e[r+t]=e[o+t],e[o+t]=n}}}function I(e,t){let n=t.length,r=e.length;if(r>0){let i=!0;for(let a=0;a<n;a++)if(e[r-n+a]!==t[a]){i=!1;break}if(i)return!1}for(let i=0;i<n;i++)e[r+i]=t[i];return!0}function Ye(e,t){let n=t.length;for(let r=0;r<n;r++)e[r]=t[r]}function L(e,t,n,r,i=[]){let a=r+t*n;for(let t=0;t<n;t++)i[t]=e[a+t];return i}function Xe(e,t,n,r,i=[]){let a,o;if(n&8)a=(r[3]-e[1])/(t[1]-e[1]),o=3;else if(n&4)a=(r[1]-e[1])/(t[1]-e[1]),o=1;else if(n&2)a=(r[2]-e[0])/(t[0]-e[0]),o=2;else if(n&1)a=(r[0]-e[0])/(t[0]-e[0]),o=0;else return null;for(let n=0;n<e.length;n++)i[n]=(o&1)===n?r[o]:a*(t[n]-e[n])+e[n];return i}function R(e,t){let n=0;return e[0]<t[0]?n|=1:e[0]>t[2]&&(n|=2),e[1]<t[1]?n|=4:e[1]>t[3]&&(n|=8),n}function Ze(e,t){let{size:n=2,broken:r=!1,gridResolution:i=10,gridOffset:a=[0,0],startIndex:o=0,endIndex:s=e.length}=t||{},c=(s-o)/n,l=[],u=[l],d=L(e,0,n,o),f,p,m=nt(d,i,a,[]),h=[];I(l,d);for(let t=1;t<c;t++){for(f=L(e,t,n,o,f),p=R(f,m);p;){Xe(d,f,p,m,h);let e=R(h,m);e&&(Xe(d,h,e,m,h),p=e),I(l,h),Ye(d,h),rt(m,i,p),r&&l.length>n&&(l=[],u.push(l),I(l,d)),p=R(f,m)}I(l,f),Ye(d,f)}return r?u:u[0]}var Qe=0,$e=1;function et(e,t=null,n){if(!e.length)return[];let{size:r=2,gridResolution:i=10,gridOffset:a=[0,0],edgeTypes:o=!1}=n||{},s=[],c=[{pos:e,types:o?Array(e.length/r).fill($e):null,holes:t||[]}],l=[[],[]],u=[];for(;c.length;){let{pos:e,types:t,holes:n}=c.shift();it(e,r,n[0]||e.length,l),u=nt(l[0],i,a,u);let d=R(l[1],u);if(d){let i=tt(e,t,r,0,n[0]||e.length,u,d),a={pos:i[0].pos,types:i[0].types,holes:[]},s={pos:i[1].pos,types:i[1].types,holes:[]};c.push(a,s);for(let c=0;c<n.length;c++)i=tt(e,t,r,n[c],n[c+1]||e.length,u,d),i[0]&&(a.holes.push(a.pos.length),a.pos=z(a.pos,i[0].pos),o&&(a.types=z(a.types,i[0].types))),i[1]&&(s.holes.push(s.pos.length),s.pos=z(s.pos,i[1].pos),o&&(s.types=z(s.types,i[1].types)))}else{let r={positions:e};o&&(r.edgeTypes=t),n.length&&(r.holeIndices=n),s.push(r)}}return s}function tt(e,t,n,r,i,a,o){let s=(i-r)/n,c=[],l=[],u=[],d=[],f=[],p,m,h,g=L(e,s-1,n,r),_=Math.sign(o&8?g[1]-a[3]:g[0]-a[2]),v=t&&t[s-1],y=0,b=0;for(let i=0;i<s;i++)p=L(e,i,n,r,p),m=Math.sign(o&8?p[1]-a[3]:p[0]-a[2]),h=t&&t[r/n+i],m&&_&&_!==m&&(Xe(g,p,o,a,f),I(c,f)&&u.push(v),I(l,f)&&d.push(v)),m<=0?(I(c,p)&&u.push(h),y-=m):u.length&&(u[u.length-1]=Qe),m>=0?(I(l,p)&&d.push(h),b+=m):d.length&&(d[d.length-1]=Qe),Ye(g,p),_=m,v=h;return[y?{pos:c,types:t&&u}:null,b?{pos:l,types:t&&d}:null]}function nt(e,t,n,r){let i=Math.floor((e[0]-n[0])/t)*t+n[0],a=Math.floor((e[1]-n[1])/t)*t+n[1];return r[0]=i,r[1]=a,r[2]=i+t,r[3]=a+t,r}function rt(e,t,n){n&8?(e[1]+=t,e[3]+=t):n&4?(e[1]-=t,e[3]-=t):n&2?(e[0]+=t,e[2]+=t):n&1&&(e[0]-=t,e[2]-=t)}function it(e,t,n,r){let i=1/0,a=-1/0,o=1/0,s=-1/0;for(let r=0;r<n;r+=t){let t=e[r],n=e[r+1];i=t<i?t:i,a=t>a?t:a,o=n<o?n:o,s=n>s?n:s}return r[0][0]=i,r[0][1]=o,r[1][0]=a,r[1][1]=s,r}function z(e,t){for(let n=0;n<t.length;n++)e.push(t[n]);return e}var at=85.051129;function ot(e,t){let{size:n=2,startIndex:r=0,endIndex:i=e.length,normalize:a=!0}=t||{},o=e.slice(r,i);ut(o,n,0,i-r);let s=Ze(o,{size:n,broken:!0,gridResolution:360,gridOffset:[-180,-180]});if(a)for(let e of s)dt(e,n);return s}function st(e,t=null,n){let{size:r=2,normalize:i=!0,edgeTypes:a=!1}=n||{};t||=[];let o=[],s=[],c=0,l=0;for(let i=0;i<=t.length;i++){let a=t[i]||e.length,u=l,d=ct(e,r,c,a);for(let t=d;t<a;t++)o[l++]=e[t];for(let t=c;t<d;t++)o[l++]=e[t];ut(o,r,u,l),lt(o,r,u,l,n?.maxLatitude),c=a,s[i]=l}s.pop();let u=et(o,s,{size:r,gridResolution:360,gridOffset:[-180,-180],edgeTypes:a});if(i)for(let e of u)dt(e.positions,r);return u}function ct(e,t,n,r){let i=-1,a=-1;for(let o=n+1;o<r;o+=t){let t=Math.abs(e[o]);t>i&&(i=t,a=o-1)}return a}function lt(e,t,n,r,i=at){let a=e[n],o=e[r-t];if(Math.abs(a-o)>180){let r=L(e,0,t,n);r[0]+=Math.round((o-a)/360)*360,I(e,r),r[1]=Math.sign(r[1])*i,I(e,r),r[0]=a,I(e,r)}}function ut(e,t,n,r){let i=e[0],a;for(let o=n;o<r;o+=t){a=e[o];let t=a-i;(t>180||t<-180)&&(a-=Math.round(t/360)*360),e[o]=i=a}}function dt(e,t){let n,r=e.length/t;for(let i=0;i<r&&(n=e[i*t],(n+180)%360==0);i++);let i=-Math.round(n/360)*360;if(i!==0)for(let n=0;n<r;n++)e[n*t]+=i}var ft=class extends l{constructor(e){let{indices:t,attributes:n}=pt(e);super({...e,indices:t,attributes:n})}};function pt(e){let{radius:t,height:r=1,nradial:i=10}=e,{vertices:a}=e;a&&(n.assert(a.length>=i),a=a.flatMap(e=>[e[0],e[1]]),We(a,Ue.COUNTER_CLOCKWISE));let o=r>0,s=i+1,c=o?s*3+1:i,l=Math.PI*2/i,u=new Uint16Array(o?i*3*2:0),d=new Float32Array(c*3),f=new Float32Array(c*3),p=0;if(o){for(let e=0;e<s;e++){let n=e*l,o=e%i,s=Math.sin(n),c=Math.cos(n);for(let e=0;e<2;e++)d[p+0]=a?a[o*2]:c*t,d[p+1]=a?a[o*2+1]:s*t,d[p+2]=(1/2-e)*r,f[p+0]=a?a[o*2]:c,f[p+1]=a?a[o*2+1]:s,p+=3}d[p+0]=d[p-3],d[p+1]=d[p-2],d[p+2]=d[p-1],p+=3}for(let e=+!o;e<s;e++){let n=Math.floor(e/2)*Math.sign(.5-e%2),o=n*l,s=(n+i)%i,c=Math.sin(o),u=Math.cos(o);d[p+0]=a?a[s*2]:u*t,d[p+1]=a?a[s*2+1]:c*t,d[p+2]=r/2,f[p+2]=1,p+=3}if(o){let e=0;for(let t=0;t<i;t++)u[e++]=t*2+0,u[e++]=t*2+2,u[e++]=t*2+0,u[e++]=t*2+1,u[e++]=t*2+1,u[e++]=t*2+3}return{indices:u,attributes:{POSITION:{size:3,value:d},NORMAL:{size:3,value:f}}}}var mt=`#version 300 es
#define SHADER_NAME column-layer-vertex-shader
in vec3 positions;
in vec3 normals;
in vec3 instancePositions;
in float instanceElevations;
in vec3 instancePositions64Low;
in vec4 instanceFillColors;
in vec4 instanceLineColors;
in float instanceStrokeWidths;
in vec3 instancePickingColors;
uniform float opacity;
uniform float radius;
uniform float angle;
uniform vec2 offset;
uniform bool extruded;
uniform bool stroked;
uniform bool isStroke;
uniform float coverage;
uniform float elevationScale;
uniform float edgeDistance;
uniform float widthScale;
uniform float widthMinPixels;
uniform float widthMaxPixels;
uniform int radiusUnits;
uniform int widthUnits;
out vec4 vColor;
#ifdef FLAT_SHADING
out vec4 position_commonspace;
#endif
void main(void) {
geometry.worldPosition = instancePositions;
vec4 color = isStroke ? instanceLineColors : instanceFillColors;
mat2 rotationMatrix = mat2(cos(angle), sin(angle), -sin(angle), cos(angle));
float elevation = 0.0;
float strokeOffsetRatio = 1.0;
if (extruded) {
elevation = instanceElevations * (positions.z + 1.0) / 2.0 * elevationScale;
} else if (stroked) {
float widthPixels = clamp(
project_size_to_pixel(instanceStrokeWidths * widthScale, widthUnits),
widthMinPixels, widthMaxPixels) / 2.0;
float halfOffset = project_pixel_size(widthPixels) / project_size(edgeDistance * coverage * radius);
if (isStroke) {
strokeOffsetRatio -= sign(positions.z) * halfOffset;
} else {
strokeOffsetRatio -= halfOffset;
}
}
float shouldRender = float(color.a > 0.0 && instanceElevations >= 0.0);
float dotRadius = radius * coverage * shouldRender;
geometry.pickingColor = instancePickingColors;
vec3 centroidPosition = vec3(instancePositions.xy, instancePositions.z + elevation);
vec3 centroidPosition64Low = instancePositions64Low;
vec2 offset = (rotationMatrix * positions.xy * strokeOffsetRatio + offset) * dotRadius;
if (radiusUnits == UNIT_METERS) {
offset = project_size(offset);
}
vec3 pos = vec3(offset, 0.);
DECKGL_FILTER_SIZE(pos, geometry);
gl_Position = project_position_to_clipspace(centroidPosition, centroidPosition64Low, pos, geometry.position);
geometry.normal = project_normal(vec3(rotationMatrix * normals.xy, normals.z));
DECKGL_FILTER_GL_POSITION(gl_Position, geometry);
if (extruded && !isStroke) {
#ifdef FLAT_SHADING
position_commonspace = geometry.position;
vColor = vec4(color.rgb, color.a * opacity);
#else
vec3 lightColor = lighting_getLightColor(color.rgb, project_uCameraPosition, geometry.position.xyz, geometry.normal);
vColor = vec4(lightColor, color.a * opacity);
#endif
} else {
vColor = vec4(color.rgb, color.a * opacity);
}
DECKGL_FILTER_COLOR(vColor, geometry);
}
`,ht=`#version 300 es
#define SHADER_NAME column-layer-fragment-shader
precision highp float;
uniform vec3 project_uCameraPosition;
uniform bool extruded;
uniform bool isStroke;
out vec4 fragColor;
in vec4 vColor;
#ifdef FLAT_SHADING
in vec4 position_commonspace;
#endif
void main(void) {
fragColor = vColor;
geometry.uv = vec2(0.);
#ifdef FLAT_SHADING
if (extruded && !isStroke && !bool(picking.isActive)) {
vec3 normal = normalize(cross(dFdx(position_commonspace.xyz), dFdy(position_commonspace.xyz)));
fragColor.rgb = lighting_getLightColor(vColor.rgb, project_uCameraPosition, position_commonspace.xyz, normal);
}
#endif
DECKGL_FILTER_COLOR(fragColor, geometry);
}
`,B=[0,0,0,255],gt={diskResolution:{type:`number`,min:4,value:20},vertices:null,radius:{type:`number`,min:0,value:1e3},angle:{type:`number`,value:0},offset:{type:`array`,value:[0,0]},coverage:{type:`number`,min:0,max:1,value:1},elevationScale:{type:`number`,min:0,value:1},radiusUnits:`meters`,lineWidthUnits:`meters`,lineWidthScale:1,lineWidthMinPixels:0,lineWidthMaxPixels:2**53-1,extruded:!0,wireframe:!1,filled:!0,stroked:!1,flatShading:!1,getPosition:{type:`accessor`,value:e=>e.position},getFillColor:{type:`accessor`,value:B},getLineColor:{type:`accessor`,value:B},getLineWidth:{type:`accessor`,value:1},getElevation:{type:`accessor`,value:1e3},material:!0,getColor:{deprecatedFor:[`getFillColor`,`getLineColor`]}},V=class extends h{getShaders(){let e={},{flatShading:t}=this.props;return t&&(e.FLAT_SHADING=1),super.getShaders({vs:mt,fs:ht,defines:e,modules:[g,t?_:r,d]})}initializeState(){this.getAttributeManager().addInstanced({instancePositions:{size:3,type:`float64`,fp64:this.use64bitPositions(),transition:!0,accessor:`getPosition`},instanceElevations:{size:1,transition:!0,accessor:`getElevation`},instanceFillColors:{size:this.props.colorFormat.length,type:`unorm8`,transition:!0,accessor:`getFillColor`,defaultValue:B},instanceLineColors:{size:this.props.colorFormat.length,type:`unorm8`,transition:!0,accessor:`getLineColor`,defaultValue:B},instanceStrokeWidths:{size:1,accessor:`getLineWidth`,transition:!0}})}updateState(e){super.updateState(e);let{props:t,oldProps:n,changeFlags:r}=e,i=r.extensionsChanged||t.flatShading!==n.flatShading;i&&(this.state.models?.forEach(e=>e.destroy()),this.setState(this._getModels()),this.getAttributeManager().invalidateAll());let a=this.getNumInstances();this.state.fillModel.setInstanceCount(a),this.state.wireframeModel.setInstanceCount(a),(i||t.diskResolution!==n.diskResolution||t.vertices!==n.vertices||(t.extruded||t.stroked)!==(n.extruded||n.stroked))&&this._updateGeometry(t)}getGeometry(e,t,n){let r=new ft({radius:1,height:n?2:0,vertices:t,nradial:e}),i=0;if(t)for(let n=0;n<e;n++){let r=t[n],a=Math.sqrt(r[0]*r[0]+r[1]*r[1]);i+=a/e}else i=1;return this.setState({edgeDistance:Math.cos(Math.PI/e)*i}),r}_getModels(){let e=this.getShaders(),t=this.getAttributeManager().getBufferLayouts(),n=new u(this.context.device,{...e,id:`${this.props.id}-fill`,bufferLayout:t,isInstanced:!0}),r=new u(this.context.device,{...e,id:`${this.props.id}-wireframe`,bufferLayout:t,isInstanced:!0});return{fillModel:n,wireframeModel:r,models:[r,n]}}_updateGeometry({diskResolution:e,vertices:t,extruded:n,stroked:r}){let i=this.getGeometry(e,t,n||r);this.setState({fillVertexCount:i.attributes.POSITION.value.length/3});let a=this.state.fillModel,o=this.state.wireframeModel;a.setGeometry(i),a.setTopology(`triangle-strip`),a.setIndexBuffer(null),o.setGeometry(i),o.setTopology(`line-list`)}draw({uniforms:e}){let{lineWidthUnits:t,lineWidthScale:n,lineWidthMinPixels:r,lineWidthMaxPixels:i,radiusUnits:o,elevationScale:s,extruded:c,filled:l,stroked:u,wireframe:d,offset:f,coverage:p,radius:m,angle:h}=this.props,g=this.state.fillModel,_=this.state.wireframeModel,{fillVertexCount:v,edgeDistance:y}=this.state,b={...e,radius:m,angle:h/180*Math.PI,offset:f,extruded:c,stroked:u,coverage:p,elevationScale:s,edgeDistance:y,radiusUnits:a[o],widthUnits:a[t],widthScale:n,widthMinPixels:r,widthMaxPixels:i};c&&d&&(_.setUniforms(b),_.setUniforms({isStroke:!0}),_.draw(this.context.renderPass)),g.setUniforms(b),l&&(g.setVertexCount(v),g.setUniforms({isStroke:!1}),g.draw(this.context.renderPass)),!c&&u&&(g.setVertexCount(v*2/3),g.setUniforms({isStroke:!0}),g.draw(this.context.renderPass))}};V.layerName=`ColumnLayer`,V.defaultProps=gt;var _t={cellSize:{type:`number`,min:0,value:1e3},offset:{type:`array`,value:[1,1]}},vt=class extends V{_updateGeometry(){let e=new y;this.state.fillModel.setGeometry(e)}draw({uniforms:e}){let{elevationScale:t,extruded:n,offset:r,coverage:i,cellSize:o,angle:s,radiusUnits:c}=this.props,l=this.state.fillModel;l.setUniforms(e),l.setUniforms({radius:o/2,radiusUnits:a[c],angle:s,offset:r,extruded:n,coverage:i,elevationScale:t,edgeDistance:1,isStroke:!1}),l.draw(this.context.renderPass)}};vt.layerName=`GridCellLayer`,vt.defaultProps=_t;function yt(e,t,n,r){let i;if(Array.isArray(e[0])){let n=e.length*t;i=Array(n);for(let n=0;n<e.length;n++)for(let r=0;r<t;r++)i[n*t+r]=e[n][r]||0}else i=e;return n?Ze(i,{size:t,gridResolution:n}):r?ot(i,{size:t}):i}var bt=1,xt=2,St=4,Ct=class extends m{constructor(e){super({...e,attributes:{positions:{size:3,padding:18,initialize:!0,type:e.fp64?Float64Array:Float32Array},segmentTypes:{size:1,type:Uint8ClampedArray}}})}get(e){return this.attributes[e]}getGeometryFromBuffer(e){return this.normalize?super.getGeometryFromBuffer(e):null}normalizeGeometry(e){return this.normalize?yt(e,this.positionSize,this.opts.resolution,this.opts.wrapLongitude):e}getGeometrySize(e){if(wt(e)){let t=0;for(let n of e)t+=this.getGeometrySize(n);return t}let t=this.getPathLength(e);return t<2?0:this.isClosed(e)?t<3?0:t+2:t}updateGeometryAttributes(e,t){if(t.geometrySize!==0)if(e&&wt(e))for(let n of e){let e=this.getGeometrySize(n);t.geometrySize=e,this.updateGeometryAttributes(n,t),t.vertexStart+=e}else this._updateSegmentTypes(e,t),this._updatePositions(e,t)}_updateSegmentTypes(e,t){let n=this.attributes.segmentTypes,r=e?this.isClosed(e):!1,{vertexStart:i,geometrySize:a}=t;n.fill(0,i,i+a),r?(n[i]=St,n[i+a-2]=St):(n[i]+=bt,n[i+a-2]+=xt),n[i+a-1]=St}_updatePositions(e,t){let{positions:n}=this.attributes;if(!n||!e)return;let{vertexStart:r,geometrySize:i}=t,a=[,,,];for(let t=r,o=0;o<i;t++,o++)this.getPointOnPath(e,o,a),n[t*3]=a[0],n[t*3+1]=a[1],n[t*3+2]=a[2]}getPathLength(e){return e.length/this.positionSize}getPointOnPath(e,t,n=[]){let{positionSize:r}=this;t*r>=e.length&&(t+=1-e.length/r);let i=t*r;return n[0]=e[i],n[1]=e[i+1],n[2]=r===3&&e[i+2]||0,n}isClosed(e){if(!this.normalize)return!!this.opts.loop;let{positionSize:t}=this,n=e.length-t;return e[0]===e[n]&&e[1]===e[n+1]&&(t===2||e[2]===e[n+2])}};function wt(e){return Array.isArray(e[0])}var Tt=`#version 300 es
#define SHADER_NAME path-layer-vertex-shader
in vec2 positions;
in float instanceTypes;
in vec3 instanceStartPositions;
in vec3 instanceEndPositions;
in vec3 instanceLeftPositions;
in vec3 instanceRightPositions;
in vec3 instanceLeftPositions64Low;
in vec3 instanceStartPositions64Low;
in vec3 instanceEndPositions64Low;
in vec3 instanceRightPositions64Low;
in float instanceStrokeWidths;
in vec4 instanceColors;
in vec3 instancePickingColors;
uniform float widthScale;
uniform float widthMinPixels;
uniform float widthMaxPixels;
uniform float jointType;
uniform float capType;
uniform float miterLimit;
uniform bool billboard;
uniform int widthUnits;
uniform float opacity;
out vec4 vColor;
out vec2 vCornerOffset;
out float vMiterLength;
out vec2 vPathPosition;
out float vPathLength;
out float vJointType;
const float EPSILON = 0.001;
const vec3 ZERO_OFFSET = vec3(0.0);
float flipIfTrue(bool flag) {
return -(float(flag) * 2. - 1.);
}
vec3 getLineJoinOffset(
vec3 prevPoint, vec3 currPoint, vec3 nextPoint,
vec2 width
) {
bool isEnd = positions.x > 0.0;
float sideOfPath = positions.y;
float isJoint = float(sideOfPath == 0.0);
vec3 deltaA3 = (currPoint - prevPoint);
vec3 deltaB3 = (nextPoint - currPoint);
mat3 rotationMatrix;
bool needsRotation = !billboard && project_needs_rotation(currPoint, rotationMatrix);
if (needsRotation) {
deltaA3 = deltaA3 * rotationMatrix;
deltaB3 = deltaB3 * rotationMatrix;
}
vec2 deltaA = deltaA3.xy / width;
vec2 deltaB = deltaB3.xy / width;
float lenA = length(deltaA);
float lenB = length(deltaB);
vec2 dirA = lenA > 0. ? normalize(deltaA) : vec2(0.0, 0.0);
vec2 dirB = lenB > 0. ? normalize(deltaB) : vec2(0.0, 0.0);
vec2 perpA = vec2(-dirA.y, dirA.x);
vec2 perpB = vec2(-dirB.y, dirB.x);
vec2 tangent = dirA + dirB;
tangent = length(tangent) > 0. ? normalize(tangent) : perpA;
vec2 miterVec = vec2(-tangent.y, tangent.x);
vec2 dir = isEnd ? dirA : dirB;
vec2 perp = isEnd ? perpA : perpB;
float L = isEnd ? lenA : lenB;
float sinHalfA = abs(dot(miterVec, perp));
float cosHalfA = abs(dot(dirA, miterVec));
float turnDirection = flipIfTrue(dirA.x * dirB.y >= dirA.y * dirB.x);
float cornerPosition = sideOfPath * turnDirection;
float miterSize = 1.0 / max(sinHalfA, EPSILON);
miterSize = mix(
min(miterSize, max(lenA, lenB) / max(cosHalfA, EPSILON)),
miterSize,
step(0.0, cornerPosition)
);
vec2 offsetVec = mix(miterVec * miterSize, perp, step(0.5, cornerPosition))
* (sideOfPath + isJoint * turnDirection);
bool isStartCap = lenA == 0.0 || (!isEnd && (instanceTypes == 1.0 || instanceTypes == 3.0));
bool isEndCap = lenB == 0.0 || (isEnd && (instanceTypes == 2.0 || instanceTypes == 3.0));
bool isCap = isStartCap || isEndCap;
if (isCap) {
offsetVec = mix(perp * sideOfPath, dir * capType * 4.0 * flipIfTrue(isStartCap), isJoint);
vJointType = capType;
} else {
vJointType = jointType;
}
vPathLength = L;
vCornerOffset = offsetVec;
vMiterLength = dot(vCornerOffset, miterVec * turnDirection);
vMiterLength = isCap ? isJoint : vMiterLength;
vec2 offsetFromStartOfPath = vCornerOffset + deltaA * float(isEnd);
vPathPosition = vec2(
dot(offsetFromStartOfPath, perp),
dot(offsetFromStartOfPath, dir)
);
geometry.uv = vPathPosition;
float isValid = step(instanceTypes, 3.5);
vec3 offset = vec3(offsetVec * width * isValid, 0.0);
if (needsRotation) {
offset = rotationMatrix * offset;
}
return offset;
}
void clipLine(inout vec4 position, vec4 refPosition) {
if (position.w < EPSILON) {
float r = (EPSILON - refPosition.w) / (position.w - refPosition.w);
position = refPosition + (position - refPosition) * r;
}
}
void main() {
geometry.pickingColor = instancePickingColors;
vColor = vec4(instanceColors.rgb, instanceColors.a * opacity);
float isEnd = positions.x;
vec3 prevPosition = mix(instanceLeftPositions, instanceStartPositions, isEnd);
vec3 prevPosition64Low = mix(instanceLeftPositions64Low, instanceStartPositions64Low, isEnd);
vec3 currPosition = mix(instanceStartPositions, instanceEndPositions, isEnd);
vec3 currPosition64Low = mix(instanceStartPositions64Low, instanceEndPositions64Low, isEnd);
vec3 nextPosition = mix(instanceEndPositions, instanceRightPositions, isEnd);
vec3 nextPosition64Low = mix(instanceEndPositions64Low, instanceRightPositions64Low, isEnd);
geometry.worldPosition = currPosition;
vec2 widthPixels = vec2(clamp(
project_size_to_pixel(instanceStrokeWidths * widthScale, widthUnits),
widthMinPixels, widthMaxPixels) / 2.0);
vec3 width;
if (billboard) {
vec4 prevPositionScreen = project_position_to_clipspace(prevPosition, prevPosition64Low, ZERO_OFFSET);
vec4 currPositionScreen = project_position_to_clipspace(currPosition, currPosition64Low, ZERO_OFFSET, geometry.position);
vec4 nextPositionScreen = project_position_to_clipspace(nextPosition, nextPosition64Low, ZERO_OFFSET);
clipLine(prevPositionScreen, currPositionScreen);
clipLine(nextPositionScreen, currPositionScreen);
clipLine(currPositionScreen, mix(nextPositionScreen, prevPositionScreen, isEnd));
width = vec3(widthPixels, 0.0);
DECKGL_FILTER_SIZE(width, geometry);
vec3 offset = getLineJoinOffset(
prevPositionScreen.xyz / prevPositionScreen.w,
currPositionScreen.xyz / currPositionScreen.w,
nextPositionScreen.xyz / nextPositionScreen.w,
project_pixel_size_to_clipspace(width.xy)
);
DECKGL_FILTER_GL_POSITION(currPositionScreen, geometry);
gl_Position = vec4(currPositionScreen.xyz + offset * currPositionScreen.w, currPositionScreen.w);
} else {
prevPosition = project_position(prevPosition, prevPosition64Low);
currPosition = project_position(currPosition, currPosition64Low);
nextPosition = project_position(nextPosition, nextPosition64Low);
width = vec3(project_pixel_size(widthPixels), 0.0);
DECKGL_FILTER_SIZE(width, geometry);
vec3 offset = getLineJoinOffset(prevPosition, currPosition, nextPosition, width.xy);
geometry.position = vec4(currPosition + offset, 1.0);
gl_Position = project_common_position_to_clipspace(geometry.position);
DECKGL_FILTER_GL_POSITION(gl_Position, geometry);
}
DECKGL_FILTER_COLOR(vColor, geometry);
}
`,Et=`#version 300 es
#define SHADER_NAME path-layer-fragment-shader
precision highp float;
uniform float miterLimit;
in vec4 vColor;
in vec2 vCornerOffset;
in float vMiterLength;
in vec2 vPathPosition;
in float vPathLength;
in float vJointType;
out vec4 fragColor;
void main(void) {
geometry.uv = vPathPosition;
if (vPathPosition.y < 0.0 || vPathPosition.y > vPathLength) {
if (vJointType > 0.5 && length(vCornerOffset) > 1.0) {
discard;
}
if (vJointType < 0.5 && vMiterLength > miterLimit + 1.0) {
discard;
}
}
fragColor = vColor;
DECKGL_FILTER_COLOR(fragColor, geometry);
}
`,Dt=[0,0,0,255],Ot={widthUnits:`meters`,widthScale:{type:`number`,min:0,value:1},widthMinPixels:{type:`number`,min:0,value:0},widthMaxPixels:{type:`number`,min:0,value:2**53-1},jointRounded:!1,capRounded:!1,miterLimit:{type:`number`,min:0,value:4},billboard:!1,_pathType:null,getPath:{type:`accessor`,value:e=>e.path},getColor:{type:`accessor`,value:Dt},getWidth:{type:`accessor`,value:1},rounded:{deprecatedFor:[`jointRounded`,`capRounded`]}},kt={enter:(e,t)=>t.length?t.subarray(t.length-e.length):e},H=class extends h{getShaders(){return super.getShaders({vs:Tt,fs:Et,modules:[g,d]})}get wrapLongitude(){return!1}getBounds(){return this.getAttributeManager()?.getBounds([`vertexPositions`])}initializeState(){this.getAttributeManager().addInstanced({vertexPositions:{size:3,vertexOffset:1,type:`float64`,fp64:this.use64bitPositions(),transition:kt,accessor:`getPath`,update:this.calculatePositions,noAlloc:!0,shaderAttributes:{instanceLeftPositions:{vertexOffset:0},instanceStartPositions:{vertexOffset:1},instanceEndPositions:{vertexOffset:2},instanceRightPositions:{vertexOffset:3}}},instanceTypes:{size:1,type:`uint8`,update:this.calculateSegmentTypes,noAlloc:!0},instanceStrokeWidths:{size:1,accessor:`getWidth`,transition:kt,defaultValue:1},instanceColors:{size:this.props.colorFormat.length,type:`unorm8`,accessor:`getColor`,transition:kt,defaultValue:Dt},instancePickingColors:{size:4,type:`uint8`,accessor:(e,{index:t,target:n})=>this.encodePickingColor(e&&e.__source?e.__source.index:t,n)}}),this.setState({pathTesselator:new Ct({fp64:this.use64bitPositions()})})}updateState(e){super.updateState(e);let{props:t,changeFlags:n}=e,r=this.getAttributeManager();if(n.dataChanged||n.updateTriggersChanged&&(n.updateTriggersChanged.all||n.updateTriggersChanged.getPath)){let{pathTesselator:e}=this.state,i=t.data.attributes||{};e.updateGeometry({data:t.data,geometryBuffer:i.getPath,buffers:i,normalize:!t._pathType,loop:t._pathType===`loop`,getGeometry:t.getPath,positionFormat:t.positionFormat,wrapLongitude:t.wrapLongitude,resolution:this.context.viewport.resolution,dataChanged:n.dataChanged}),this.setState({numInstances:e.instanceCount,startIndices:e.vertexStarts}),n.dataChanged||r.invalidateAll()}n.extensionsChanged&&(this.state.model?.destroy(),this.state.model=this._getModel(),r.invalidateAll())}getPickingInfo(e){let t=super.getPickingInfo(e),{index:n}=t,r=this.props.data;return r[0]&&r[0].__source&&(t.object=r.find(e=>e.__source.index===n)),t}disablePickingIndex(e){let t=this.props.data;if(t[0]&&t[0].__source)for(let n=0;n<t.length;n++)t[n].__source.index===e&&this._disablePickingIndex(n);else super.disablePickingIndex(e)}draw({uniforms:e}){let{jointRounded:t,capRounded:n,billboard:r,miterLimit:i,widthUnits:o,widthScale:s,widthMinPixels:c,widthMaxPixels:l}=this.props,u=this.state.model;u.setUniforms(e),u.setUniforms({jointType:Number(t),capType:Number(n),billboard:r,widthUnits:a[o],widthScale:s,miterLimit:i,widthMinPixels:c,widthMaxPixels:l}),u.draw(this.context.renderPass)}_getModel(){let e=[0,1,2,1,4,2,1,3,4,3,5,4],t=[0,0,0,-1,0,1,1,-1,1,1,1,0];return new u(this.context.device,{...this.getShaders(),id:this.props.id,bufferLayout:this.getAttributeManager().getBufferLayouts(),geometry:new l({topology:`triangle-list`,attributes:{indices:new Uint16Array(e),positions:{value:new Float32Array(t),size:2}}}),isInstanced:!0})}calculatePositions(e){let{pathTesselator:t}=this.state;e.startIndices=t.vertexStarts,e.value=t.get(`positions`)}calculateSegmentTypes(e){let{pathTesselator:t}=this.state;e.startIndices=t.vertexStarts,e.value=t.get(`segmentTypes`)}};H.defaultProps=Ot,H.layerName=`PathLayer`;var At=e(t(((e,t)=>{t.exports=n,t.exports.default=n;function n(e,t,n){n||=2;var i=t&&t.length,o=i?t[0]*n:e.length,s=r(e,0,o,n,!0),c=[];if(!s||s.next===s.prev)return c;var l,d,f,p,m,h,g;if(i&&(s=u(e,t,s,n)),e.length>80*n){l=f=e[0],d=p=e[1];for(var _=n;_<o;_+=n)m=e[_],h=e[_+1],m<l&&(l=m),h<d&&(d=h),m>f&&(f=m),h>p&&(p=h);g=Math.max(f-l,p-d),g=g===0?0:32767/g}return a(s,c,n,l,d,g,0),c}function r(e,t,n,r,i){var a,o;if(i===N(e,t,n,r)>0)for(a=t;a<n;a+=r)o=A(a,e[a],e[a+1],o);else for(a=n-r;a>=t;a-=r)o=A(a,e[a],e[a+1],o);return o&&S(o,o.next)&&(j(o),o=o.next),o}function i(e,t){if(!e)return e;t||=e;var n=e,r;do if(r=!1,!n.steiner&&(S(n,n.next)||x(n.prev,n,n.next)===0)){if(j(n),n=t=n.prev,n===n.next)break;r=!0}else n=n.next;while(r||n!==t);return t}function a(e,t,n,r,u,d,f){if(e){!f&&d&&h(e,r,u,d);for(var p=e,m,g;e.prev!==e.next;){if(m=e.prev,g=e.next,d?s(e,r,u,d):o(e)){t.push(m.i/n|0),t.push(e.i/n|0),t.push(g.i/n|0),j(e),e=g.next,p=g.next;continue}if(e=g,e===p){f?f===1?(e=c(i(e),t,n),a(e,t,n,r,u,d,2)):f===2&&l(e,t,n,r,u,d):a(i(e),t,n,r,u,d,1);break}}}}function o(e){var t=e.prev,n=e,r=e.next;if(x(t,n,r)>=0)return!1;for(var i=t.x,a=n.x,o=r.x,s=t.y,c=n.y,l=r.y,u=i<a?i<o?i:o:a<o?a:o,d=s<c?s<l?s:l:c<l?c:l,f=i>a?i>o?i:o:a>o?a:o,p=s>c?s>l?s:l:c>l?c:l,m=r.next;m!==t;){if(m.x>=u&&m.x<=f&&m.y>=d&&m.y<=p&&y(i,s,a,c,o,l,m.x,m.y)&&x(m.prev,m,m.next)>=0)return!1;m=m.next}return!0}function s(e,t,n,r){var i=e.prev,a=e,o=e.next;if(x(i,a,o)>=0)return!1;for(var s=i.x,c=a.x,l=o.x,u=i.y,d=a.y,f=o.y,p=s<c?s<l?s:l:c<l?c:l,m=u<d?u<f?u:f:d<f?d:f,h=s>c?s>l?s:l:c>l?c:l,g=u>d?u>f?u:f:d>f?d:f,v=_(p,m,t,n,r),b=_(h,g,t,n,r),S=e.prevZ,C=e.nextZ;S&&S.z>=v&&C&&C.z<=b;){if(S.x>=p&&S.x<=h&&S.y>=m&&S.y<=g&&S!==i&&S!==o&&y(s,u,c,d,l,f,S.x,S.y)&&x(S.prev,S,S.next)>=0||(S=S.prevZ,C.x>=p&&C.x<=h&&C.y>=m&&C.y<=g&&C!==i&&C!==o&&y(s,u,c,d,l,f,C.x,C.y)&&x(C.prev,C,C.next)>=0))return!1;C=C.nextZ}for(;S&&S.z>=v;){if(S.x>=p&&S.x<=h&&S.y>=m&&S.y<=g&&S!==i&&S!==o&&y(s,u,c,d,l,f,S.x,S.y)&&x(S.prev,S,S.next)>=0)return!1;S=S.prevZ}for(;C&&C.z<=b;){if(C.x>=p&&C.x<=h&&C.y>=m&&C.y<=g&&C!==i&&C!==o&&y(s,u,c,d,l,f,C.x,C.y)&&x(C.prev,C,C.next)>=0)return!1;C=C.nextZ}return!0}function c(e,t,n){var r=e;do{var a=r.prev,o=r.next.next;!S(a,o)&&C(a,r,r.next,o)&&D(a,o)&&D(o,a)&&(t.push(a.i/n|0),t.push(r.i/n|0),t.push(o.i/n|0),j(r),j(r.next),r=e=o),r=r.next}while(r!==e);return i(r)}function l(e,t,n,r,o,s){var c=e;do{for(var l=c.next.next;l!==c.prev;){if(c.i!==l.i&&b(c,l)){var u=k(c,l);c=i(c,c.next),u=i(u,u.next),a(c,t,n,r,o,s,0),a(u,t,n,r,o,s,0);return}l=l.next}c=c.next}while(c!==e)}function u(e,t,n,i){var a=[],o,s,c,l,u;for(o=0,s=t.length;o<s;o++)c=t[o]*i,l=o<s-1?t[o+1]*i:e.length,u=r(e,c,l,i,!1),u===u.next&&(u.steiner=!0),a.push(v(u));for(a.sort(d),o=0;o<a.length;o++)n=f(a[o],n);return n}function d(e,t){return e.x-t.x}function f(e,t){var n=p(e,t);if(!n)return t;var r=k(n,e);return i(r,r.next),i(n,n.next)}function p(e,t){var n=t,r=e.x,i=e.y,a=-1/0,o;do{if(i<=n.y&&i>=n.next.y&&n.next.y!==n.y){var s=n.x+(i-n.y)*(n.next.x-n.x)/(n.next.y-n.y);if(s<=r&&s>a&&(a=s,o=n.x<n.next.x?n:n.next,s===r))return o}n=n.next}while(n!==t);if(!o)return null;var c=o,l=o.x,u=o.y,d=1/0,f;n=o;do r>=n.x&&n.x>=l&&r!==n.x&&y(i<u?r:a,i,l,u,i<u?a:r,i,n.x,n.y)&&(f=Math.abs(i-n.y)/(r-n.x),D(n,e)&&(f<d||f===d&&(n.x>o.x||n.x===o.x&&m(o,n)))&&(o=n,d=f)),n=n.next;while(n!==c);return o}function m(e,t){return x(e.prev,e,t.prev)<0&&x(t.next,e,e.next)<0}function h(e,t,n,r){var i=e;do i.z===0&&(i.z=_(i.x,i.y,t,n,r)),i.prevZ=i.prev,i.nextZ=i.next,i=i.next;while(i!==e);i.prevZ.nextZ=null,i.prevZ=null,g(i)}function g(e){var t,n,r,i,a,o,s,c,l=1;do{for(n=e,e=null,a=null,o=0;n;){for(o++,r=n,s=0,t=0;t<l&&(s++,r=r.nextZ,r);t++);for(c=l;s>0||c>0&&r;)s!==0&&(c===0||!r||n.z<=r.z)?(i=n,n=n.nextZ,s--):(i=r,r=r.nextZ,c--),a?a.nextZ=i:e=i,i.prevZ=a,a=i;n=r}a.nextZ=null,l*=2}while(o>1);return e}function _(e,t,n,r,i){return e=(e-n)*i|0,t=(t-r)*i|0,e=(e|e<<8)&16711935,e=(e|e<<4)&252645135,e=(e|e<<2)&858993459,e=(e|e<<1)&1431655765,t=(t|t<<8)&16711935,t=(t|t<<4)&252645135,t=(t|t<<2)&858993459,t=(t|t<<1)&1431655765,e|t<<1}function v(e){var t=e,n=e;do(t.x<n.x||t.x===n.x&&t.y<n.y)&&(n=t),t=t.next;while(t!==e);return n}function y(e,t,n,r,i,a,o,s){return(i-o)*(t-s)>=(e-o)*(a-s)&&(e-o)*(r-s)>=(n-o)*(t-s)&&(n-o)*(a-s)>=(i-o)*(r-s)}function b(e,t){return e.next.i!==t.i&&e.prev.i!==t.i&&!E(e,t)&&(D(e,t)&&D(t,e)&&O(e,t)&&(x(e.prev,e,t.prev)||x(e,t.prev,t))||S(e,t)&&x(e.prev,e,e.next)>0&&x(t.prev,t,t.next)>0)}function x(e,t,n){return(t.y-e.y)*(n.x-t.x)-(t.x-e.x)*(n.y-t.y)}function S(e,t){return e.x===t.x&&e.y===t.y}function C(e,t,n,r){var i=T(x(e,t,n)),a=T(x(e,t,r)),o=T(x(n,r,e)),s=T(x(n,r,t));return!!(i!==a&&o!==s||i===0&&w(e,n,t)||a===0&&w(e,r,t)||o===0&&w(n,e,r)||s===0&&w(n,t,r))}function w(e,t,n){return t.x<=Math.max(e.x,n.x)&&t.x>=Math.min(e.x,n.x)&&t.y<=Math.max(e.y,n.y)&&t.y>=Math.min(e.y,n.y)}function T(e){return e>0?1:e<0?-1:0}function E(e,t){var n=e;do{if(n.i!==e.i&&n.next.i!==e.i&&n.i!==t.i&&n.next.i!==t.i&&C(n,n.next,e,t))return!0;n=n.next}while(n!==e);return!1}function D(e,t){return x(e.prev,e,e.next)<0?x(e,t,e.next)>=0&&x(e,e.prev,t)>=0:x(e,t,e.prev)<0||x(e,e.next,t)<0}function O(e,t){var n=e,r=!1,i=(e.x+t.x)/2,a=(e.y+t.y)/2;do n.y>a!=n.next.y>a&&n.next.y!==n.y&&i<(n.next.x-n.x)*(a-n.y)/(n.next.y-n.y)+n.x&&(r=!r),n=n.next;while(n!==e);return r}function k(e,t){var n=new M(e.i,e.x,e.y),r=new M(t.i,t.x,t.y),i=e.next,a=t.prev;return e.next=t,t.prev=e,n.next=i,i.prev=n,r.next=n,n.prev=r,a.next=r,r.prev=a,r}function A(e,t,n,r){var i=new M(e,t,n);return r?(i.next=r.next,i.prev=r,r.next.prev=i,r.next=i):(i.prev=i,i.next=i),i}function j(e){e.next.prev=e.prev,e.prev.next=e.next,e.prevZ&&(e.prevZ.nextZ=e.nextZ),e.nextZ&&(e.nextZ.prevZ=e.prevZ)}function M(e,t,n){this.i=e,this.x=t,this.y=n,this.prev=null,this.next=null,this.z=0,this.prevZ=null,this.nextZ=null,this.steiner=!1}n.deviation=function(e,t,n,r){var i=t&&t.length,a=i?t[0]*n:e.length,o=Math.abs(N(e,0,a,n));if(i)for(var s=0,c=t.length;s<c;s++){var l=t[s]*n,u=s<c-1?t[s+1]*n:e.length;o-=Math.abs(N(e,l,u,n))}var d=0;for(s=0;s<r.length;s+=3){var f=r[s]*n,p=r[s+1]*n,m=r[s+2]*n;d+=Math.abs((e[f]-e[m])*(e[p+1]-e[f+1])-(e[f]-e[p])*(e[m+1]-e[f+1]))}return o===0&&d===0?0:Math.abs((d-o)/o)};function N(e,t,n,r){for(var i=0,a=t,o=n-r;a<n;a+=r)i+=(e[o]-e[a])*(e[a+1]+e[o+1]),o=a;return i}n.flatten=function(e){for(var t=e[0][0].length,n={vertices:[],holes:[],dimensions:t},r=0,i=0;i<e.length;i++){for(var a=0;a<e[i].length;a++)for(var o=0;o<t;o++)n.vertices.push(e[i][a][o]);i>0&&(r+=e[i-1].length,n.holes.push(r))}return n}}))(),1),U=Ue.CLOCKWISE,jt=Ue.COUNTER_CLOCKWISE,W={isClosed:!0};function Mt(e){if(e=e&&e.positions||e,!Array.isArray(e)&&!ArrayBuffer.isView(e))throw Error(`invalid polygon`)}function G(e){return`positions`in e?e.positions:e}function K(e){return`holeIndices`in e?e.holeIndices:null}function Nt(e){return Array.isArray(e[0])}function Pt(e){return e.length>=1&&e[0].length>=2&&Number.isFinite(e[0][0])}function Ft(e){let t=e[0],n=e[e.length-1];return t[0]===n[0]&&t[1]===n[1]&&t[2]===n[2]}function It(e,t,n,r){for(let i=0;i<t;i++)if(e[n+i]!==e[r-t+i])return!1;return!0}function Lt(e,t,n,r,i){let a=t,o=n.length;for(let t=0;t<o;t++)for(let i=0;i<r;i++)e[a++]=n[t][i]||0;if(!Ft(n))for(let t=0;t<r;t++)e[a++]=n[0][t]||0;return W.start=t,W.end=a,W.size=r,We(e,i,W),a}function Rt(e,t,n,r,i=0,a,o){a||=n.length;let s=a-i;if(s<=0)return t;let c=t;for(let t=0;t<s;t++)e[c++]=n[i+t];if(!It(n,r,i,a))for(let t=0;t<r;t++)e[c++]=n[i+t];return W.start=t,W.end=c,W.size=r,We(e,o,W),c}function zt(e,t){Mt(e);let n=[],r=[];if(`positions`in e){let{positions:i,holeIndices:a}=e;if(a){let e=0;for(let o=0;o<=a.length;o++)e=Rt(n,e,i,t,a[o-1],a[o],o===0?U:jt),r.push(e);return r.pop(),{positions:n,holeIndices:r}}e=i}if(!Nt(e))return Rt(n,0,e,t,0,n.length,U),n;if(!Pt(e)){let i=0;for(let[a,o]of e.entries())i=Lt(n,i,o,t,a===0?U:jt),r.push(i);return r.pop(),{positions:n,holeIndices:r}}return Lt(n,0,e,t,U),n}function Bt(e,t,n){let r=e.length/3,i=0;for(let a=0;a<r;a++){let o=(a+1)%r;i+=e[a*3+t]*e[o*3+n],i-=e[o*3+t]*e[a*3+n]}return Math.abs(i/2)}function Vt(e,t,n,r){let i=e.length/3;for(let a=0;a<i;a++){let i=a*3,o=e[i+0],s=e[i+1],c=e[i+2];e[i+t]=o,e[i+n]=s,e[i+r]=c}}function Ht(e,t,n,r){let i=K(e);i&&=i.map(e=>e/t);let a=G(e),o=r&&t===3;if(n){let e=a.length;a=a.slice();let r=[];for(let i=0;i<e;i+=t){r[0]=a[i],r[1]=a[i+1],o&&(r[2]=a[i+2]);let e=n(r);a[i]=e[0],a[i+1]=e[1],o&&(a[i+2]=e[2])}}if(o){let e=Bt(a,0,1),t=Bt(a,0,2),r=Bt(a,1,2);if(!e&&!t&&!r)return[];e>t&&e>r||(t>r?(n||(a=a.slice()),Vt(a,0,2,1)):(n||(a=a.slice()),Vt(a,2,0,1)))}return(0,At.default)(a,i,t)}var Ut=class extends m{constructor(e){let{fp64:t,IndexType:n=Uint32Array}=e;super({...e,attributes:{positions:{size:3,type:t?Float64Array:Float32Array},vertexValid:{type:Uint16Array,size:1},indices:{type:n,size:1}}})}get(e){let{attributes:t}=this;return e===`indices`?t.indices&&t.indices.subarray(0,this.vertexCount):t[e]}updateGeometry(e){super.updateGeometry(e);let t=this.buffers.indices;if(t)this.vertexCount=(t.value||t).length;else if(this.data&&!this.getGeometry)throw Error(`missing indices buffer`)}normalizeGeometry(e){if(this.normalize){let t=zt(e,this.positionSize);return this.opts.resolution?et(G(t),K(t),{size:this.positionSize,gridResolution:this.opts.resolution,edgeTypes:!0}):this.opts.wrapLongitude?st(G(t),K(t),{size:this.positionSize,maxLatitude:86,edgeTypes:!0}):t}return e}getGeometrySize(e){if(Wt(e)){let t=0;for(let n of e)t+=this.getGeometrySize(n);return t}return G(e).length/this.positionSize}getGeometryFromBuffer(e){return this.normalize||!this.buffers.indices?super.getGeometryFromBuffer(e):null}updateGeometryAttributes(e,t){if(e&&Wt(e))for(let n of e){let e=this.getGeometrySize(n);t.geometrySize=e,this.updateGeometryAttributes(n,t),t.vertexStart+=e,t.indexStart=this.indexStarts[t.geometryIndex+1]}else{let n=e;this._updateIndices(n,t),this._updatePositions(n,t),this._updateVertexValid(n,t)}}_updateIndices(e,{geometryIndex:t,vertexStart:n,indexStart:r}){let{attributes:i,indexStarts:a,typedArrayManager:o}=this,s=i.indices;if(!s||!e)return;let c=r,l=Ht(e,this.positionSize,this.opts.preproject,this.opts.full3d);s=o.allocate(s,r+l.length,{copy:!0});for(let e=0;e<l.length;e++)s[c++]=l[e]+n;a[t+1]=r+l.length,i.indices=s}_updatePositions(e,{vertexStart:t,geometrySize:n}){let{attributes:{positions:r},positionSize:i}=this;if(!r||!e)return;let a=G(e);for(let e=t,o=0;o<n;e++,o++){let t=a[o*i],n=a[o*i+1],s=i>2?a[o*i+2]:0;r[e*3]=t,r[e*3+1]=n,r[e*3+2]=s}}_updateVertexValid(e,{vertexStart:t,geometrySize:n}){let{positionSize:r}=this,i=this.attributes.vertexValid,a=e&&K(e);if(e&&e.edgeTypes?i.set(e.edgeTypes,t):i.fill(1,t,t+n),a)for(let e=0;e<a.length;e++)i[t+a[e]/r-1]=0;i[t+n-1]=0}};function Wt(e){return Array.isArray(e)&&e.length>0&&!Number.isFinite(e[0])}var Gt=`uniform bool extruded;
uniform bool isWireframe;
uniform float elevationScale;
uniform float opacity;
in vec4 fillColors;
in vec4 lineColors;
in vec3 pickingColors;
out vec4 vColor;
struct PolygonProps {
vec3 positions;
vec3 positions64Low;
vec3 normal;
float elevations;
};
vec3 project_offset_normal(vec3 vector) {
if (project_uCoordinateSystem == COORDINATE_SYSTEM_LNGLAT ||
project_uCoordinateSystem == COORDINATE_SYSTEM_LNGLAT_OFFSETS) {
return normalize(vector * project_uCommonUnitsPerWorldUnit);
}
return project_normal(vector);
}
void calculatePosition(PolygonProps props) {
vec3 pos = props.positions;
vec3 pos64Low = props.positions64Low;
vec3 normal = props.normal;
vec4 colors = isWireframe ? lineColors : fillColors;
geometry.worldPosition = props.positions;
geometry.pickingColor = pickingColors;
if (extruded) {
pos.z += props.elevations * elevationScale;
}
gl_Position = project_position_to_clipspace(pos, pos64Low, vec3(0.), geometry.position);
DECKGL_FILTER_GL_POSITION(gl_Position, geometry);
if (extruded) {
#ifdef IS_SIDE_VERTEX
normal = project_offset_normal(normal);
#else
normal = project_normal(normal);
#endif
geometry.normal = normal;
vec3 lightColor = lighting_getLightColor(colors.rgb, project_uCameraPosition, geometry.position.xyz, geometry.normal);
vColor = vec4(lightColor, colors.a * opacity);
} else {
vColor = vec4(colors.rgb, colors.a * opacity);
}
DECKGL_FILTER_COLOR(vColor, geometry);
}
`,Kt=`\
#version 300 es
#define SHADER_NAME solid-polygon-layer-vertex-shader
in vec3 vertexPositions;
in vec3 vertexPositions64Low;
in float elevations;
${Gt}
void main(void) {
PolygonProps props;
props.positions = vertexPositions;
props.positions64Low = vertexPositions64Low;
props.elevations = elevations;
props.normal = vec3(0.0, 0.0, 1.0);
calculatePosition(props);
}
`,qt=`\
#version 300 es
#define SHADER_NAME solid-polygon-layer-vertex-shader-side
#define IS_SIDE_VERTEX
in vec2 positions;
in vec3 vertexPositions;
in vec3 nextVertexPositions;
in vec3 vertexPositions64Low;
in vec3 nextVertexPositions64Low;
in float elevations;
in float instanceVertexValid;
${Gt}
void main(void) {
if(instanceVertexValid < 0.5){
gl_Position = vec4(0.);
return;
}
PolygonProps props;
vec3 pos;
vec3 pos64Low;
vec3 nextPos;
vec3 nextPos64Low;
#if RING_WINDING_ORDER_CW == 1
pos = vertexPositions;
pos64Low = vertexPositions64Low;
nextPos = nextVertexPositions;
nextPos64Low = nextVertexPositions64Low;
#else
pos = nextVertexPositions;
pos64Low = nextVertexPositions64Low;
nextPos = vertexPositions;
nextPos64Low = vertexPositions64Low;
#endif
props.positions = mix(pos, nextPos, positions.x);
props.positions64Low = mix(pos64Low, nextPos64Low, positions.x);
props.normal = vec3(
pos.y - nextPos.y + (pos64Low.y - nextPos64Low.y),
nextPos.x - pos.x + (nextPos64Low.x - pos64Low.x),
0.0);
props.elevations = elevations * positions.y;
calculatePosition(props);
}
`,Jt=`#version 300 es
#define SHADER_NAME solid-polygon-layer-fragment-shader
precision highp float;
in vec4 vColor;
out vec4 fragColor;
void main(void) {
fragColor = vColor;
geometry.uv = vec2(0.);
DECKGL_FILTER_COLOR(fragColor, geometry);
}
`,q=[0,0,0,255],Yt={filled:!0,extruded:!1,wireframe:!1,_normalize:!0,_windingOrder:`CW`,_full3d:!1,elevationScale:{type:`number`,min:0,value:1},getPolygon:{type:`accessor`,value:e=>e.polygon},getElevation:{type:`accessor`,value:1e3},getFillColor:{type:`accessor`,value:q},getLineColor:{type:`accessor`,value:q},material:!0},J={enter:(e,t)=>t.length?t.subarray(t.length-e.length):e},Y=class extends h{getShaders(e){return super.getShaders({vs:e===`top`?Kt:qt,fs:Jt,defines:{RING_WINDING_ORDER_CW:!this.props._normalize&&this.props._windingOrder===`CCW`?0:1},modules:[g,r,d]})}get wrapLongitude(){return!1}getBounds(){return this.getAttributeManager()?.getBounds([`vertexPositions`])}initializeState(){let{viewport:e}=this.context,{coordinateSystem:t}=this.props,{_full3d:n}=this.props;e.isGeospatial&&t===v.DEFAULT&&(t=v.LNGLAT);let r;t===v.LNGLAT&&(r=n?e.projectPosition.bind(e):e.projectFlat.bind(e)),this.setState({numInstances:0,polygonTesselator:new Ut({preproject:r,fp64:this.use64bitPositions(),IndexType:Uint32Array})});let i=this.getAttributeManager();i.remove([`instancePickingColors`]),i.add({indices:{size:1,isIndexed:!0,update:this.calculateIndices,noAlloc:!0},vertexPositions:{size:3,type:`float64`,stepMode:`dynamic`,fp64:this.use64bitPositions(),transition:J,accessor:`getPolygon`,update:this.calculatePositions,noAlloc:!0,shaderAttributes:{nextVertexPositions:{vertexOffset:1}}},instanceVertexValid:{size:1,type:`uint16`,stepMode:`instance`,update:this.calculateVertexValid,noAlloc:!0},elevations:{size:1,stepMode:`dynamic`,transition:J,accessor:`getElevation`},fillColors:{size:this.props.colorFormat.length,type:`unorm8`,stepMode:`dynamic`,transition:J,accessor:`getFillColor`,defaultValue:q},lineColors:{size:this.props.colorFormat.length,type:`unorm8`,stepMode:`dynamic`,transition:J,accessor:`getLineColor`,defaultValue:q},pickingColors:{size:4,type:`uint8`,stepMode:`dynamic`,accessor:(e,{index:t,target:n})=>this.encodePickingColor(e&&e.__source?e.__source.index:t,n)}})}getPickingInfo(e){let t=super.getPickingInfo(e),{index:n}=t,r=this.props.data;return r[0]&&r[0].__source&&(t.object=r.find(e=>e.__source.index===n)),t}disablePickingIndex(e){let t=this.props.data;if(t[0]&&t[0].__source)for(let n=0;n<t.length;n++)t[n].__source.index===e&&this._disablePickingIndex(n);else super.disablePickingIndex(e)}draw({uniforms:e}){let{extruded:t,filled:n,wireframe:r,elevationScale:i}=this.props,{topModel:a,sideModel:o,wireframeModel:s,polygonTesselator:c}=this.state,l={...e,extruded:!!t,elevationScale:i};s&&r&&(s.setInstanceCount(c.instanceCount-1),s.setUniforms(l),s.draw(this.context.renderPass)),o&&n&&(o.setInstanceCount(c.instanceCount-1),o.setUniforms(l),o.draw(this.context.renderPass)),a&&n&&(a.setVertexCount(c.vertexCount),a.setUniforms(l),a.draw(this.context.renderPass))}updateState(e){super.updateState(e),this.updateGeometry(e);let{props:t,oldProps:n,changeFlags:r}=e,i=this.getAttributeManager();(r.extensionsChanged||t.filled!==n.filled||t.extruded!==n.extruded)&&(this.state.models?.forEach(e=>e.destroy()),this.setState(this._getModels()),i.invalidateAll())}updateGeometry({props:e,oldProps:t,changeFlags:n}){if(n.dataChanged||n.updateTriggersChanged&&(n.updateTriggersChanged.all||n.updateTriggersChanged.getPolygon)){let{polygonTesselator:t}=this.state,r=e.data.attributes||{};t.updateGeometry({data:e.data,normalize:e._normalize,geometryBuffer:r.getPolygon,buffers:r,getGeometry:e.getPolygon,positionFormat:e.positionFormat,wrapLongitude:e.wrapLongitude,resolution:this.context.viewport.resolution,fp64:this.use64bitPositions(),dataChanged:n.dataChanged,full3d:e._full3d}),this.setState({numInstances:t.instanceCount,startIndices:t.vertexStarts}),n.dataChanged||this.getAttributeManager().invalidateAll()}}_getModels(){let{id:e,filled:t,extruded:n}=this.props,r,i,a;if(t){let t=this.getShaders(`top`);t.defines.NON_INSTANCED_MODEL=1;let n=this.getAttributeManager().getBufferLayouts({isInstanced:!1});r=new u(this.context.device,{...t,id:`${e}-top`,topology:`triangle-list`,uniforms:{isWireframe:!1},bufferLayout:n,isIndexed:!0,userData:{excludeAttributes:{instanceVertexValid:!0}}})}if(n){let t=this.getAttributeManager().getBufferLayouts({isInstanced:!0});i=new u(this.context.device,{...this.getShaders(`side`),id:`${e}-side`,bufferLayout:t,uniforms:{isWireframe:!1},geometry:new l({topology:`triangle-strip`,attributes:{positions:{size:2,value:new Float32Array([1,0,0,0,1,1,0,1])}}}),isInstanced:!0,userData:{excludeAttributes:{indices:!0}}}),a=new u(this.context.device,{...this.getShaders(`side`),id:`${e}-wireframe`,bufferLayout:t,uniforms:{isWireframe:!0},geometry:new l({topology:`line-strip`,attributes:{positions:{size:2,value:new Float32Array([1,0,0,0,0,1,1,1])}}}),isInstanced:!0,userData:{excludeAttributes:{indices:!0}}})}return{models:[i,a,r].filter(Boolean),topModel:r,sideModel:i,wireframeModel:a}}calculateIndices(e){let{polygonTesselator:t}=this.state;e.startIndices=t.indexStarts,e.value=t.get(`indices`)}calculatePositions(e){let{polygonTesselator:t}=this.state;e.startIndices=t.vertexStarts,e.value=t.get(`positions`)}calculateVertexValid(e){e.value=this.state.polygonTesselator.get(`vertexValid`)}};Y.defaultProps=Yt,Y.layerName=`SolidPolygonLayer`;function Xt({data:e,getIndex:t,dataRange:n,replace:r}){let{startRow:i=0,endRow:a=1/0}=n,o=e.length,s=o,c=o;for(let n=0;n<o;n++){let r=t(e[n]);if(s>n&&r>=i&&(s=n),r>=a){c=n;break}}let l=s,u=c-s===r.length?void 0:e.slice(c);for(let t=0;t<r.length;t++)e[l++]=r[t];if(u){for(let t=0;t<u.length;t++)e[l++]=u[t];e.length=l}return{startRow:s,endRow:s+r.length}}var Zt=[0,0,0,255],Qt={stroked:!0,filled:!0,extruded:!1,elevationScale:1,wireframe:!1,_normalize:!0,_windingOrder:`CW`,lineWidthUnits:`meters`,lineWidthScale:1,lineWidthMinPixels:0,lineWidthMaxPixels:2**53-1,lineJointRounded:!1,lineMiterLimit:4,getPolygon:{type:`accessor`,value:e=>e.polygon},getFillColor:{type:`accessor`,value:[0,0,0,255]},getLineColor:{type:`accessor`,value:Zt},getLineWidth:{type:`accessor`,value:1},getElevation:{type:`accessor`,value:1e3},material:!0},$t=class extends s{initializeState(){this.state={paths:[],pathsDiff:null},this.props.getLineDashArray&&n.removed(`getLineDashArray`,`PathStyleExtension`)()}updateState({changeFlags:e}){let t=e.dataChanged||e.updateTriggersChanged&&(e.updateTriggersChanged.all||e.updateTriggersChanged.getPolygon);if(t&&Array.isArray(e.dataChanged)){let t=this.state.paths.slice(),n=e.dataChanged.map(e=>Xt({data:t,getIndex:e=>e.__source.index,dataRange:e,replace:this._getPaths(e)}));this.setState({paths:t,pathsDiff:n})}else t&&this.setState({paths:this._getPaths(),pathsDiff:null})}_getPaths(e={}){let{data:t,getPolygon:n,positionFormat:r,_normalize:i}=this.props,a=[],o=r===`XY`?2:3,{startRow:s,endRow:l}=e,{iterable:u,objectInfo:d}=c(t,s,l);for(let e of u){d.index++;let t=n(e,d);i&&(t=zt(t,o));let{holeIndices:r}=t,s=t.positions||t;if(r)for(let t=0;t<=r.length;t++){let n=s.slice(r[t-1]||0,r[t]||s.length);a.push(this.getSubLayerRow({path:n},e,d.index))}else a.push(this.getSubLayerRow({path:s},e,d.index))}return a}renderLayers(){let{data:e,_dataDiff:t,stroked:n,filled:r,extruded:i,wireframe:a,_normalize:o,_windingOrder:s,elevationScale:c,transitions:l,positionFormat:u}=this.props,{lineWidthUnits:d,lineWidthScale:f,lineWidthMinPixels:p,lineWidthMaxPixels:m,lineJointRounded:h,lineMiterLimit:g,lineDashJustified:_}=this.props,{getFillColor:v,getLineColor:y,getLineWidth:b,getLineDashArray:x,getElevation:S,getPolygon:C,updateTriggers:w,material:T}=this.props,{paths:E,pathsDiff:D}=this.state,O=this.getSubLayerClass(`fill`,Y),k=this.getSubLayerClass(`stroke`,H),A=this.shouldRenderSubLayer(`fill`,E)&&new O({_dataDiff:t,extruded:i,elevationScale:c,filled:r,wireframe:a,_normalize:o,_windingOrder:s,getElevation:S,getFillColor:v,getLineColor:i&&a?y:Zt,material:T,transitions:l},this.getSubLayerProps({id:`fill`,updateTriggers:w&&{getPolygon:w.getPolygon,getElevation:w.getElevation,getFillColor:w.getFillColor,lineColors:i&&a,getLineColor:w.getLineColor}}),{data:e,positionFormat:u,getPolygon:C}),j=!i&&n&&this.shouldRenderSubLayer(`stroke`,E)&&new k({_dataDiff:D&&(()=>D),widthUnits:d,widthScale:f,widthMinPixels:p,widthMaxPixels:m,jointRounded:h,miterLimit:g,dashJustified:_,_pathType:`loop`,transitions:l&&{getWidth:l.getLineWidth,getColor:l.getLineColor,getPath:l.getPolygon},getColor:this.getSubLayerAccessor(y),getWidth:this.getSubLayerAccessor(b),getDashArray:this.getSubLayerAccessor(x)},this.getSubLayerProps({id:`stroke`,updateTriggers:w&&{getWidth:w.getLineWidth,getColor:w.getLineColor,getDashArray:w.getLineDashArray}}),{data:E,positionFormat:u,getPath:e=>e.path});return[!i&&A,j,i&&A]}};$t.layerName=`PolygonLayer`,$t.defaultProps=Qt;function en(e,t){if(!e)return null;let n=`startIndices`in e?e.startIndices[t]:t,r=e.featureIds.value[n];return n===-1?null:tn(e,r,n)}function tn(e,t,n){let r={properties:{...e.properties[t]}};for(let t in e.numericProps)r.properties[t]=e.numericProps[t].value[n];return r}function nn(e,t){let n={points:null,lines:null,polygons:null};for(let r in n){let i=e[r].globalFeatureIds.value;n[r]=new Uint8ClampedArray(i.length*4);let a=[];for(let e=0;e<i.length;e++)t(i[e],a),n[r][e*4+0]=a[0],n[r][e*4+1]=a[1],n[r][e*4+2]=a[2],n[r][e*4+3]=255}return n}var rn=`#version 300 es
#define SHADER_NAME multi-icon-layer-fragment-shader
precision highp float;
uniform float opacity;
uniform sampler2D iconsTexture;
uniform float gamma;
uniform bool sdf;
uniform float alphaCutoff;
uniform float sdfBuffer;
uniform float outlineBuffer;
uniform vec4 outlineColor;
in vec4 vColor;
in vec2 vTextureCoords;
in vec2 uv;
out vec4 fragColor;
void main(void) {
geometry.uv = uv;
if (!bool(picking.isActive)) {
float alpha = texture(iconsTexture, vTextureCoords).a;
vec4 color = vColor;
if (sdf) {
float distance = alpha;
alpha = smoothstep(sdfBuffer - gamma, sdfBuffer + gamma, distance);
if (outlineBuffer > 0.0) {
float inFill = alpha;
float inBorder = smoothstep(outlineBuffer - gamma, outlineBuffer + gamma, distance);
color = mix(outlineColor, vColor, inFill);
alpha = inBorder;
}
}
float a = alpha * color.a;
if (a < alphaCutoff) {
discard;
}
fragColor = vec4(color.rgb, a * opacity);
}
DECKGL_FILTER_COLOR(fragColor, geometry);
}
`,an=192/256,on=[],sn={getIconOffsets:{type:`accessor`,value:e=>e.offsets},alphaCutoff:.001,smoothing:.1,outlineWidth:0,outlineColor:{type:`color`,value:[0,0,0,255]}},X=class extends F{getShaders(){return{...super.getShaders(),fs:rn}}initializeState(){super.initializeState(),this.getAttributeManager().addInstanced({instanceOffsets:{size:2,accessor:`getIconOffsets`},instancePickingColors:{type:`uint8`,size:3,accessor:(e,{index:t,target:n})=>this.encodePickingColor(t,n)}})}updateState(e){super.updateState(e);let{props:t,oldProps:r}=e,{outlineColor:i}=t;i!==r.outlineColor&&(i=i.map(e=>e/255),i[3]=Number.isFinite(i[3])?i[3]:1,this.setState({outlineColor:i})),!t.sdf&&t.outlineWidth&&n.warn(`${this.id}: fontSettings.sdf is required to render outline`)()}draw(e){let{sdf:t,smoothing:n,outlineWidth:r}=this.props,{outlineColor:i}=this.state,a=r?Math.max(n,an*(1-r)):-1;if(e.uniforms={...e.uniforms,sdfBuffer:an,outlineBuffer:a,gamma:n,sdf:!!t,outlineColor:i},super.draw(e),t&&r){let{iconManager:e}=this.state,t=e.getTexture(),n=this.state.model;t&&(n.setUniforms({outlineBuffer:an}),n.draw(this.context.renderPass))}}getInstanceOffset(e){return e?Array.from(e).flatMap(e=>super.getInstanceOffset(e)):on}getInstanceColorMode(e){return 1}getInstanceIconFrame(e){return e?Array.from(e).flatMap(e=>super.getInstanceIconFrame(e)):on}};X.defaultProps=sn,X.layerName=`MultiIconLayer`;var Z=0x56bc75e2d63100000,cn=new Float64Array(256);for(let e=0;e<256;e++){let t=.5-(e/255)**(1/2.2);cn[e]=t*Math.abs(t)}cn[255]=-Z;var ln=class{constructor({fontSize:e=24,buffer:t=3,radius:n=8,cutoff:r=.25,fontFamily:i=`sans-serif`,fontWeight:a=`normal`,fontStyle:o=`normal`,lang:s=null}={}){this.buffer=t,this.radius=n,this.cutoff=r,this.lang=s;let c=this.size=e+t*4,l=this._createCanvas(c),u=this.ctx=l.getContext(`2d`,{willReadFrequently:!0});u.font=`${o} ${a} ${e}px ${i}`,u.textBaseline=`alphabetic`,u.textAlign=`left`,u.fillStyle=`black`,this.gridOuter=new Float64Array(c*c),this.gridInner=new Float64Array(c*c),this.f=new Float64Array(c),this.z=new Float64Array(c+1),this.v=new Uint16Array(c)}_createCanvas(e){if(typeof OffscreenCanvas<`u`)return new OffscreenCanvas(e,e);let t=document.createElement(`canvas`);return t.width=t.height=e,t}draw(e){let{width:t,actualBoundingBoxAscent:n,actualBoundingBoxDescent:r,actualBoundingBoxLeft:i,actualBoundingBoxRight:a}=this.ctx.measureText(e),o=Math.ceil(n),s=Math.floor(-i),c=Math.max(0,Math.min(this.size-this.buffer,Math.ceil(a)-s)),l=Math.max(0,Math.min(this.size-this.buffer,o+Math.ceil(r))),u=c+2*this.buffer,d=l+2*this.buffer,f=Math.max(u*d,0),p=new Uint8ClampedArray(f),m={data:p,width:u,height:d,glyphWidth:c,glyphHeight:l,glyphTop:o,glyphLeft:s,glyphAdvance:t};if(c===0||l===0)return m;let{ctx:h,buffer:g,gridInner:_,gridOuter:v}=this;this.lang&&(h.lang=this.lang),h.clearRect(g,g,c,l),h.fillText(e,g-s,g+o);let y=h.getImageData(g,g,c,l);v.fill(Z,0,f),_.fill(0,0,f);let b=3;for(let e=0;e<l;e++){let t=(e+g)*u+g;for(let e=0;e<c;e++,b+=4,t++){let e=y.data[b];if(e===0)continue;let n=cn[e];v[t]=Math.max(0,n),_[t]=Math.max(0,-n)}}un(v,0,0,u,d,u,this.f,this.v,this.z);let x=Math.min(g,1);un(_,g-x,g-x,c+2*x,l+2*x,u,this.f,this.v,this.z);let S=255/this.radius,C=255*(1-this.cutoff);for(let e=0;e<f;e++){let t=Math.sqrt(v[e])-Math.sqrt(_[e]);p[e]=Math.round(C-S*t)}return m}};function un(e,t,n,r,i,a,o,s,c){for(let l=t;l<t+r;l++)dn(e,n*a+l,a,i,o,s,c);for(let l=n;l<n+i;l++)dn(e,l*a+t,1,r,o,s,c)}function dn(e,t,n,r,i,a,o){a[0]=0,o[0]=-Z,o[1]=Z,i[0]=e[t];for(let s=1,c=0,l=0;s<r;s++){i[s]=e[t+s*n];let r=s*s;do{let e=a[c];l=(i[s]-i[e]+r-e*e)/(s-e)/2}while(l<=o[c]&&--c>-1);c++,a[c]=s,o[c]=l,o[c+1]=Z}for(let s=0,c=0;s<r;s++){for(;o[c+1]<s;)c++;let r=a[c],l=s-r;e[t+s*n]=i[r]+l*l}}var fn=32,pn=[];function mn(e){return 2**Math.ceil(Math.log2(e))}function hn({characterSet:e,getFontWidth:t,fontHeight:n,buffer:r,maxCanvasWidth:i,mapping:a={},xOffset:o=0,yOffset:s=0}){let c=0,l=o,u=n+r*2;for(let o of e)if(!a[o]){let e=t(o);l+e+r*2>i&&(l=0,c++),a[o]={x:l+r,y:s+c*u+r,width:e,height:u,layoutWidth:e,layoutHeight:n},l+=e+r*2}return{mapping:a,xOffset:l,yOffset:s+c*u,canvasHeight:mn(s+(c+1)*u)}}function gn(e,t,n,r){let i=0;for(let a=t;a<n;a++){let t=e[a];i+=r[t]?.layoutWidth||0}return i}function _n(e,t,n,r,i,a){let o=t,s=0;for(let c=t;c<n;c++){let t=gn(e,c,c+1,i);s+t>r&&(o<c&&a.push(c),o=c,s=0),s+=t}return s}function vn(e,t,n,r,i,a){let o=t,s=t,c=t,l=0;for(let u=t;u<n;u++)if((e[u]===` `||e[u+1]===` `||u+1===n)&&(c=u+1),c>s){let t=gn(e,s,c,i);l+t>r&&(o<s&&(a.push(s),o=s,l=0),t>r&&(t=_n(e,s,c,r,i,a),o=a[a.length-1])),s=c,l+=t}return l}function yn(e,t,n,r,i=0,a){a===void 0&&(a=e.length);let o=[];return t===`break-all`?_n(e,i,a,n,r,o):vn(e,i,a,n,r,o),o}function bn(e,t,r,i,a,o){let s=0,c=0;for(let o=t;o<r;o++){let t=e[o],r=i[t];r?(c||=r.layoutHeight,a[o]=s+r.layoutWidth/2,s+=r.layoutWidth):(n.warn(`Missing character: ${t} (${t.codePointAt(0)})`)(),a[o]=s,s+=fn)}o[0]=s,o[1]=c}function xn(e,t,n,r,i){let a=Array.from(e),o=a.length,s=Array(o),c=Array(o),l=Array(o),u=(n===`break-word`||n===`break-all`)&&isFinite(r)&&r>0,d=[0,0],f=[0,0],p=0,m=0,h=0;for(let e=0;e<=o;e++){let g=a[e];if((g===`
`||e===o)&&(h=e),h>m){let e=u?yn(a,n,r,i,m,h):pn;for(let n=0;n<=e.length;n++){let r=n===0?m:e[n-1],o=n<e.length?e[n]:h;bn(a,r,o,i,s,f);for(let e=r;e<o;e++){let t=i[a[e]]?.layoutOffsetY||0;c[e]=p+f[1]/2+t,l[e]=f[0]}p+=f[1]*t,d[0]=Math.max(d[0],f[0])}m=h}g===`
`&&(s[m]=0,c[m]=0,l[m]=0,m++)}return d[1]=p,{x:s,y:c,rowWidth:l,size:d}}function Sn({value:e,length:t,stride:n,offset:r,startIndices:i,characterSet:a}){let o=e.BYTES_PER_ELEMENT,s=n?n/o:1,c=r?r/o:0,l=i[t]||Math.ceil((e.length-c)/s),u=a&&new Set,d=Array(t),f=e;if(s>1||c>0){let t=e.constructor;f=new t(l);for(let t=0;t<l;t++)f[t]=e[t*s+c]}for(let e=0;e<t;e++){let t=i[e],n=i[e+1]||l,r=f.subarray(t,n);d[e]=String.fromCodePoint.apply(null,r),u&&r.forEach(u.add,u)}if(u)for(let e of u)a.add(String.fromCodePoint(e));return{texts:d,characterCount:l}}var Cn=class{constructor(e=5){this._cache={},this._order=[],this.limit=e}get(e){let t=this._cache[e];return t&&(this._deleteOrder(e),this._appendOrder(e)),t}set(e,t){this._cache[e]?(this.delete(e),this._cache[e]=t,this._appendOrder(e)):(Object.keys(this._cache).length===this.limit&&this.delete(this._order[0]),this._cache[e]=t,this._appendOrder(e))}delete(e){this._cache[e]&&(delete this._cache[e],this._deleteOrder(e))}_deleteOrder(e){let t=this._order.indexOf(e);t>=0&&this._order.splice(t,1)}_appendOrder(e){this._order.push(e)}};function wn(){let e=[];for(let t=32;t<128;t++)e.push(String.fromCharCode(t));return e}var Q={fontFamily:`Monaco, monospace`,fontWeight:`normal`,characterSet:wn(),fontSize:64,buffer:4,sdf:!1,cutoff:.25,radius:12,smoothing:.1},Tn=1024,En=.9,Dn=1.2,On=3,kn=new Cn(On);function An(e,t){let n;n=typeof t==`string`?new Set(Array.from(t)):new Set(t);let r=kn.get(e);if(!r)return n;for(let e in r.mapping)n.has(e)&&n.delete(e);return n}function jn(e,t){for(let n=0;n<e.length;n++)t.data[4*n+3]=e[n]}function Mn(e,t,n,r){e.font=`${r} ${n}px ${t}`,e.fillStyle=`#000`,e.textBaseline=`alphabetic`,e.textAlign=`left`}function Nn(e){n.assert(Number.isFinite(e)&&e>=On,`Invalid cache limit`),kn=new Cn(e)}var Pn=class{constructor(){this.props={...Q}}get atlas(){return this._atlas}get mapping(){return this._atlas&&this._atlas.mapping}get scale(){let{fontSize:e,buffer:t}=this.props;return(e*Dn+t*2)/e}setProps(e={}){Object.assign(this.props,e),this._key=this._getKey();let t=An(this._key,this.props.characterSet),n=kn.get(this._key);if(n&&t.size===0){this._atlas!==n&&(this._atlas=n);return}let r=this._generateFontAtlas(t,n);this._atlas=r,kn.set(this._key,r)}_generateFontAtlas(e,t){let{fontFamily:n,fontWeight:r,fontSize:i,buffer:a,sdf:o,radius:s,cutoff:c}=this.props,l=t&&t.data;l||(l=document.createElement(`canvas`),l.width=Tn);let u=l.getContext(`2d`,{willReadFrequently:!0});Mn(u,n,i,r);let{mapping:d,canvasHeight:f,xOffset:p,yOffset:m}=hn({getFontWidth:e=>u.measureText(e).width,fontHeight:i*Dn,buffer:a,characterSet:e,maxCanvasWidth:Tn,...t&&{mapping:t.mapping,xOffset:t.xOffset,yOffset:t.yOffset}});if(l.height!==f){let e=u.getImageData(0,0,l.width,l.height);l.height=f,u.putImageData(e,0,0)}if(Mn(u,n,i,r),o){let t=new ln({fontSize:i,buffer:a,radius:s,cutoff:c,fontFamily:n,fontWeight:`${r}`});for(let n of e){let{data:e,width:r,height:a,glyphTop:o}=t.draw(n);d[n].width=r,d[n].layoutOffsetY=i*En-o;let s=u.createImageData(r,a);jn(e,s),u.putImageData(s,d[n].x,d[n].y)}}else for(let t of e)u.fillText(t,d[t].x,d[t].y+a+i*En);return{xOffset:p,yOffset:m,mapping:d,data:l,width:l.width,height:l.height}}_getKey(){let{fontFamily:e,fontWeight:t,fontSize:n,buffer:r,sdf:i,radius:a,cutoff:o}=this.props;return i?`${e} ${t} ${n} ${r} ${a} ${o}`:`${e} ${t} ${n} ${r}`}},Fn=`#version 300 es
#define SHADER_NAME text-background-layer-vertex-shader
in vec2 positions;
in vec3 instancePositions;
in vec3 instancePositions64Low;
in vec4 instanceRects;
in float instanceSizes;
in float instanceAngles;
in vec2 instancePixelOffsets;
in float instanceLineWidths;
in vec4 instanceFillColors;
in vec4 instanceLineColors;
in vec3 instancePickingColors;
uniform bool billboard;
uniform float opacity;
uniform float sizeScale;
uniform float sizeMinPixels;
uniform float sizeMaxPixels;
uniform vec4 padding;
uniform int sizeUnits;
out vec4 vFillColor;
out vec4 vLineColor;
out float vLineWidth;
out vec2 uv;
out vec2 dimensions;
vec2 rotate_by_angle(vec2 vertex, float angle) {
float angle_radian = radians(angle);
float cos_angle = cos(angle_radian);
float sin_angle = sin(angle_radian);
mat2 rotationMatrix = mat2(cos_angle, -sin_angle, sin_angle, cos_angle);
return rotationMatrix * vertex;
}
void main(void) {
geometry.worldPosition = instancePositions;
geometry.uv = positions;
geometry.pickingColor = instancePickingColors;
uv = positions;
vLineWidth = instanceLineWidths;
float sizePixels = clamp(
project_size_to_pixel(instanceSizes * sizeScale, sizeUnits),
sizeMinPixels, sizeMaxPixels
);
dimensions = instanceRects.zw * sizePixels + padding.xy + padding.zw;
vec2 pixelOffset = (positions * instanceRects.zw + instanceRects.xy) * sizePixels + mix(-padding.xy, padding.zw, positions);
pixelOffset = rotate_by_angle(pixelOffset, instanceAngles);
pixelOffset += instancePixelOffsets;
pixelOffset.y *= -1.0;
if (billboard)  {
gl_Position = project_position_to_clipspace(instancePositions, instancePositions64Low, vec3(0.0), geometry.position);
DECKGL_FILTER_GL_POSITION(gl_Position, geometry);
vec3 offset = vec3(pixelOffset, 0.0);
DECKGL_FILTER_SIZE(offset, geometry);
gl_Position.xy += project_pixel_size_to_clipspace(offset.xy);
} else {
vec3 offset_common = vec3(project_pixel_size(pixelOffset), 0.0);
DECKGL_FILTER_SIZE(offset_common, geometry);
gl_Position = project_position_to_clipspace(instancePositions, instancePositions64Low, offset_common, geometry.position);
DECKGL_FILTER_GL_POSITION(gl_Position, geometry);
}
vFillColor = vec4(instanceFillColors.rgb, instanceFillColors.a * opacity);
DECKGL_FILTER_COLOR(vFillColor, geometry);
vLineColor = vec4(instanceLineColors.rgb, instanceLineColors.a * opacity);
DECKGL_FILTER_COLOR(vLineColor, geometry);
}
`,In=`#version 300 es
#define SHADER_NAME text-background-layer-fragment-shader
precision highp float;
uniform bool stroked;
in vec4 vFillColor;
in vec4 vLineColor;
in float vLineWidth;
in vec2 uv;
in vec2 dimensions;
out vec4 fragColor;
void main(void) {
geometry.uv = uv;
vec2 pixelPosition = uv * dimensions;
if (stroked) {
float distToEdge = min(
min(pixelPosition.x, dimensions.x - pixelPosition.x),
min(pixelPosition.y, dimensions.y - pixelPosition.y)
);
float isBorder = smoothedge(distToEdge, vLineWidth);
fragColor = mix(vFillColor, vLineColor, isBorder);
} else {
fragColor = vFillColor;
}
DECKGL_FILTER_COLOR(fragColor, geometry);
}
`,Ln={billboard:!0,sizeScale:1,sizeUnits:`pixels`,sizeMinPixels:0,sizeMaxPixels:2**53-1,padding:{type:`array`,value:[0,0,0,0]},getPosition:{type:`accessor`,value:e=>e.position},getSize:{type:`accessor`,value:1},getAngle:{type:`accessor`,value:0},getPixelOffset:{type:`accessor`,value:[0,0]},getBoundingRect:{type:`accessor`,value:[0,0,0,0]},getFillColor:{type:`accessor`,value:[0,0,0,255]},getLineColor:{type:`accessor`,value:[0,0,0,255]},getLineWidth:{type:`accessor`,value:1}},Rn=class extends h{getShaders(){return super.getShaders({vs:Fn,fs:In,modules:[g,d]})}initializeState(){this.getAttributeManager().addInstanced({instancePositions:{size:3,type:`float64`,fp64:this.use64bitPositions(),transition:!0,accessor:`getPosition`},instanceSizes:{size:1,transition:!0,accessor:`getSize`,defaultValue:1},instanceAngles:{size:1,transition:!0,accessor:`getAngle`},instanceRects:{size:4,accessor:`getBoundingRect`},instancePixelOffsets:{size:2,transition:!0,accessor:`getPixelOffset`},instanceFillColors:{size:4,transition:!0,type:`unorm8`,accessor:`getFillColor`,defaultValue:[0,0,0,255]},instanceLineColors:{size:4,transition:!0,type:`unorm8`,accessor:`getLineColor`,defaultValue:[0,0,0,255]},instanceLineWidths:{size:1,transition:!0,accessor:`getLineWidth`,defaultValue:1}})}updateState(e){super.updateState(e);let{changeFlags:t}=e;t.extensionsChanged&&(this.state.model?.destroy(),this.state.model=this._getModel(),this.getAttributeManager().invalidateAll())}draw({uniforms:e}){let{billboard:t,sizeScale:n,sizeUnits:r,sizeMinPixels:i,sizeMaxPixels:o,getLineWidth:s}=this.props,{padding:c}=this.props;c.length<4&&(c=[c[0],c[1],c[0],c[1]]);let l=this.state.model;l.setUniforms(e),l.setUniforms({billboard:t,stroked:!!s,padding:c,sizeUnits:a[r],sizeScale:n,sizeMinPixels:i,sizeMaxPixels:o}),l.draw(this.context.renderPass)}_getModel(){let e=[0,0,1,0,1,1,0,1];return new u(this.context.device,{...this.getShaders(),id:this.props.id,bufferLayout:this.getAttributeManager().getBufferLayouts(),geometry:new l({topology:`triangle-fan-webgl`,vertexCount:4,attributes:{positions:{size:2,value:new Float32Array(e)}}}),isInstanced:!0})}};Rn.defaultProps=Ln,Rn.layerName=`TextBackgroundLayer`;var zn={start:1,middle:0,end:-1},Bn={top:1,center:0,bottom:-1},Vn=[0,0,0,255],Hn={billboard:!0,sizeScale:1,sizeUnits:`pixels`,sizeMinPixels:0,sizeMaxPixels:2**53-1,background:!1,getBackgroundColor:{type:`accessor`,value:[255,255,255,255]},getBorderColor:{type:`accessor`,value:Vn},getBorderWidth:{type:`accessor`,value:0},backgroundPadding:{type:`array`,value:[0,0,0,0]},characterSet:{type:`object`,value:Q.characterSet},fontFamily:Q.fontFamily,fontWeight:Q.fontWeight,lineHeight:1,outlineWidth:{type:`number`,value:0,min:0},outlineColor:{type:`color`,value:Vn},fontSettings:{type:`object`,value:{},compare:1},wordBreak:`break-word`,maxWidth:{type:`number`,value:-1},getText:{type:`accessor`,value:e=>e.text},getPosition:{type:`accessor`,value:e=>e.position},getColor:{type:`accessor`,value:Vn},getSize:{type:`accessor`,value:32},getAngle:{type:`accessor`,value:0},getTextAnchor:{type:`accessor`,value:`middle`},getAlignmentBaseline:{type:`accessor`,value:`center`},getPixelOffset:{type:`accessor`,value:[0,0]},backgroundColor:{deprecatedFor:[`background`,`getBackgroundColor`]}},Un=class extends s{constructor(){super(...arguments),this.getBoundingRect=(e,t)=>{let{size:[n,r]}=this.transformParagraph(e,t),{fontSize:i}=this.state.fontAtlasManager.props;n/=i,r/=i;let{getTextAnchor:a,getAlignmentBaseline:o}=this.props,s=zn[typeof a==`function`?a(e,t):a],c=Bn[typeof o==`function`?o(e,t):o];return[(s-1)*n/2,(c-1)*r/2,n,r]},this.getIconOffsets=(e,t)=>{let{getTextAnchor:n,getAlignmentBaseline:r}=this.props,{x:i,y:a,rowWidth:o,size:[s,c]}=this.transformParagraph(e,t),l=zn[typeof n==`function`?n(e,t):n],u=Bn[typeof r==`function`?r(e,t):r],d=i.length,f=Array(d*2),p=0;for(let e=0;e<d;e++){let t=(1-l)*(s-o[e])/2;f[p++]=(l-1)*s/2+t+i[e],f[p++]=(u-1)*c/2+a[e]}return f}}initializeState(){this.state={styleVersion:0,fontAtlasManager:new Pn},this.props.maxWidth>0&&n.warn(`v8.9 breaking change: TextLayer maxWidth is now relative to text size`)()}updateState(e){let{props:t,oldProps:n,changeFlags:r}=e;(r.dataChanged||r.updateTriggersChanged&&(r.updateTriggersChanged.all||r.updateTriggersChanged.getText))&&this._updateText(),(this._updateFontAtlas()||t.lineHeight!==n.lineHeight||t.wordBreak!==n.wordBreak||t.maxWidth!==n.maxWidth)&&this.setState({styleVersion:this.state.styleVersion+1})}getPickingInfo({info:e}){return e.object=e.index>=0?this.props.data[e.index]:null,e}_updateFontAtlas(){let{fontSettings:e,fontFamily:t,fontWeight:n}=this.props,{fontAtlasManager:r,characterSet:i}=this.state,a={...e,characterSet:i,fontFamily:t,fontWeight:n};if(!r.mapping)return r.setProps(a),!0;for(let e in a)if(a[e]!==r.props[e])return r.setProps(a),!0;return!1}_updateText(){let{data:e,characterSet:t}=this.props,n=e.attributes?.getText,{getText:r}=this.props,i=e.startIndices,a,o=t===`auto`&&new Set;if(n&&i){let{texts:t,characterCount:s}=Sn({...ArrayBuffer.isView(n)?{value:n}:n,length:e.length,startIndices:i,characterSet:o});a=s,r=(e,{index:n})=>t[n]}else{let{iterable:t,objectInfo:n}=c(e);i=[0],a=0;for(let e of t){n.index++;let t=Array.from(r(e,n)||``);o&&t.forEach(o.add,o),a+=t.length,i.push(a)}}this.setState({getText:r,startIndices:i,numInstances:a,characterSet:o||t})}transformParagraph(e,t){let{fontAtlasManager:n}=this.state,r=n.mapping,i=this.state.getText,{wordBreak:a,lineHeight:o,maxWidth:s}=this.props;return xn(i(e,t)||``,o,a,s*n.props.fontSize,r)}renderLayers(){let{startIndices:e,numInstances:t,getText:n,fontAtlasManager:{scale:r,atlas:i,mapping:a},styleVersion:o}=this.state,{data:s,_dataDiff:c,getPosition:l,getColor:u,getSize:d,getAngle:f,getPixelOffset:p,getBackgroundColor:m,getBorderColor:h,getBorderWidth:g,backgroundPadding:_,background:v,billboard:y,fontSettings:b,outlineWidth:x,outlineColor:S,sizeScale:C,sizeUnits:w,sizeMinPixels:T,sizeMaxPixels:E,transitions:D,updateTriggers:O}=this.props,k=this.getSubLayerClass(`characters`,X),A=this.getSubLayerClass(`background`,Rn);return[v&&new A({getFillColor:m,getLineColor:h,getLineWidth:g,padding:_,getPosition:l,getSize:d,getAngle:f,getPixelOffset:p,billboard:y,sizeScale:C,sizeUnits:w,sizeMinPixels:T,sizeMaxPixels:E,transitions:D&&{getPosition:D.getPosition,getAngle:D.getAngle,getSize:D.getSize,getFillColor:D.getBackgroundColor,getLineColor:D.getBorderColor,getLineWidth:D.getBorderWidth,getPixelOffset:D.getPixelOffset}},this.getSubLayerProps({id:`background`,updateTriggers:{getPosition:O.getPosition,getAngle:O.getAngle,getSize:O.getSize,getFillColor:O.getBackgroundColor,getLineColor:O.getBorderColor,getLineWidth:O.getBorderWidth,getPixelOffset:O.getPixelOffset,getBoundingRect:{getText:O.getText,getTextAnchor:O.getTextAnchor,getAlignmentBaseline:O.getAlignmentBaseline,styleVersion:o}}}),{data:s.attributes&&s.attributes.background?{length:s.length,attributes:s.attributes.background}:s,_dataDiff:c,autoHighlight:!1,getBoundingRect:this.getBoundingRect}),new k({sdf:b.sdf,smoothing:Number.isFinite(b.smoothing)?b.smoothing:Q.smoothing,outlineWidth:x/(b.radius||Q.radius),outlineColor:S,iconAtlas:i,iconMapping:a,getPosition:l,getColor:u,getSize:d,getAngle:f,getPixelOffset:p,billboard:y,sizeScale:C*r,sizeUnits:w,sizeMinPixels:T*r,sizeMaxPixels:E*r,transitions:D&&{getPosition:D.getPosition,getAngle:D.getAngle,getColor:D.getColor,getSize:D.getSize,getPixelOffset:D.getPixelOffset}},this.getSubLayerProps({id:`characters`,updateTriggers:{all:O.getText,getPosition:O.getPosition,getAngle:O.getAngle,getColor:O.getColor,getSize:O.getSize,getPixelOffset:O.getPixelOffset,getIconOffsets:{getTextAnchor:O.getTextAnchor,getAlignmentBaseline:O.getAlignmentBaseline,styleVersion:o}}}),{data:s,_dataDiff:c,startIndices:e,numInstances:t,getIconOffsets:this.getIconOffsets,getIcon:n})]}static set fontAtlasCacheLimit(e){Nn(e)}};Un.defaultProps=Hn,Un.layerName=`TextLayer`;var Wn={circle:{type:He,props:{filled:`filled`,stroked:`stroked`,lineWidthMaxPixels:`lineWidthMaxPixels`,lineWidthMinPixels:`lineWidthMinPixels`,lineWidthScale:`lineWidthScale`,lineWidthUnits:`lineWidthUnits`,pointRadiusMaxPixels:`radiusMaxPixels`,pointRadiusMinPixels:`radiusMinPixels`,pointRadiusScale:`radiusScale`,pointRadiusUnits:`radiusUnits`,pointAntialiasing:`antialiasing`,pointBillboard:`billboard`,getFillColor:`getFillColor`,getLineColor:`getLineColor`,getLineWidth:`getLineWidth`,getPointRadius:`getRadius`}},icon:{type:F,props:{iconAtlas:`iconAtlas`,iconMapping:`iconMapping`,iconSizeMaxPixels:`sizeMaxPixels`,iconSizeMinPixels:`sizeMinPixels`,iconSizeScale:`sizeScale`,iconSizeUnits:`sizeUnits`,iconAlphaCutoff:`alphaCutoff`,iconBillboard:`billboard`,getIcon:`getIcon`,getIconAngle:`getAngle`,getIconColor:`getColor`,getIconPixelOffset:`getPixelOffset`,getIconSize:`getSize`}},text:{type:Un,props:{textSizeMaxPixels:`sizeMaxPixels`,textSizeMinPixels:`sizeMinPixels`,textSizeScale:`sizeScale`,textSizeUnits:`sizeUnits`,textBackground:`background`,textBackgroundPadding:`backgroundPadding`,textFontFamily:`fontFamily`,textFontWeight:`fontWeight`,textLineHeight:`lineHeight`,textMaxWidth:`maxWidth`,textOutlineColor:`outlineColor`,textOutlineWidth:`outlineWidth`,textWordBreak:`wordBreak`,textCharacterSet:`characterSet`,textBillboard:`billboard`,textFontSettings:`fontSettings`,getText:`getText`,getTextAngle:`getAngle`,getTextColor:`getColor`,getTextPixelOffset:`getPixelOffset`,getTextSize:`getSize`,getTextAnchor:`getTextAnchor`,getTextAlignmentBaseline:`getAlignmentBaseline`,getTextBackgroundColor:`getBackgroundColor`,getTextBorderColor:`getBorderColor`,getTextBorderWidth:`getBorderWidth`}}},Gn={type:H,props:{lineWidthUnits:`widthUnits`,lineWidthScale:`widthScale`,lineWidthMinPixels:`widthMinPixels`,lineWidthMaxPixels:`widthMaxPixels`,lineJointRounded:`jointRounded`,lineCapRounded:`capRounded`,lineMiterLimit:`miterLimit`,lineBillboard:`billboard`,getLineColor:`getColor`,getLineWidth:`getWidth`}},Kn={type:Y,props:{extruded:`extruded`,filled:`filled`,wireframe:`wireframe`,elevationScale:`elevationScale`,material:`material`,_full3d:`_full3d`,getElevation:`getElevation`,getFillColor:`getFillColor`,getLineColor:`getLineColor`}};function $({type:e,props:t}){let n={};for(let r in t)n[r]=e.defaultProps[t[r]];return n}function qn(e,t){let{transitions:n,updateTriggers:r}=e.props,i={updateTriggers:{},transitions:n&&{getPosition:n.geometry}};for(let a in t){let o=t[a],s=e.props[a];a.startsWith(`get`)&&(s=e.getSubLayerAccessor(s),i.updateTriggers[o]=r[a],n&&(i.transitions[o]=n[a])),i[o]=s}return i}function Jn(e){if(Array.isArray(e))return e;switch(n.assert(e.type,`GeoJSON does not have type`),e.type){case`Feature`:return[e];case`FeatureCollection`:return n.assert(Array.isArray(e.features),`GeoJSON does not have features array`),e.features;default:return[{geometry:e}]}}function Yn(e,t,r={}){let i={pointFeatures:[],lineFeatures:[],polygonFeatures:[],polygonOutlineFeatures:[]},{startRow:a=0,endRow:o=e.length}=r;for(let r=a;r<o;r++){let a=e[r],{geometry:o}=a;if(o)if(o.type===`GeometryCollection`){n.assert(Array.isArray(o.geometries),`GeoJSON does not have geometries array`);let{geometries:e}=o;for(let n=0;n<e.length;n++){let o=e[n];Xn(o,i,t,a,r)}}else Xn(o,i,t,a,r)}return i}function Xn(e,t,r,i,a){let{type:o,coordinates:s}=e,{pointFeatures:c,lineFeatures:l,polygonFeatures:u,polygonOutlineFeatures:d}=t;if(!Qn(o,s)){n.warn(`${o} coordinates are malformed`)();return}switch(o){case`Point`:c.push(r({geometry:e},i,a));break;case`MultiPoint`:s.forEach(e=>{c.push(r({geometry:{type:`Point`,coordinates:e}},i,a))});break;case`LineString`:l.push(r({geometry:e},i,a));break;case`MultiLineString`:s.forEach(e=>{l.push(r({geometry:{type:`LineString`,coordinates:e}},i,a))});break;case`Polygon`:u.push(r({geometry:e},i,a)),s.forEach(e=>{d.push(r({geometry:{type:`LineString`,coordinates:e}},i,a))});break;case`MultiPolygon`:s.forEach(e=>{u.push(r({geometry:{type:`Polygon`,coordinates:e}},i,a)),e.forEach(e=>{d.push(r({geometry:{type:`LineString`,coordinates:e}},i,a))})});break;default:}}var Zn={Point:1,MultiPoint:2,LineString:2,MultiLineString:3,Polygon:3,MultiPolygon:4};function Qn(e,t){let r=Zn[e];for(n.assert(r,`Unknown GeoJSON type ${e}`);t&&--r>0;)t=t[0];return t&&Number.isFinite(t[0])}function $n(){return{points:{},lines:{},polygons:{},polygonsOutline:{}}}function er(e){return e.geometry.coordinates}function tr(e,t){let n=$n(),{pointFeatures:r,lineFeatures:i,polygonFeatures:a,polygonOutlineFeatures:o}=e;return n.points.data=r,n.points._dataDiff=t.pointFeatures&&(()=>t.pointFeatures),n.points.getPosition=er,n.lines.data=i,n.lines._dataDiff=t.lineFeatures&&(()=>t.lineFeatures),n.lines.getPath=er,n.polygons.data=a,n.polygons._dataDiff=t.polygonFeatures&&(()=>t.polygonFeatures),n.polygons.getPolygon=er,n.polygonsOutline.data=o,n.polygonsOutline._dataDiff=t.polygonOutlineFeatures&&(()=>t.polygonOutlineFeatures),n.polygonsOutline.getPath=er,n}function nr(e,t){let n=$n(),{points:r,lines:i,polygons:a}=e,o=nn(e,t);return n.points.data={length:r.positions.value.length/r.positions.size,attributes:{...r.attributes,getPosition:r.positions,instancePickingColors:{size:4,value:o.points}},properties:r.properties,numericProps:r.numericProps,featureIds:r.featureIds},n.lines.data={length:i.pathIndices.value.length-1,startIndices:i.pathIndices.value,attributes:{...i.attributes,getPath:i.positions,instancePickingColors:{size:4,value:o.lines}},properties:i.properties,numericProps:i.numericProps,featureIds:i.featureIds},n.lines._pathType=`open`,n.polygons.data={length:a.polygonIndices.value.length-1,startIndices:a.polygonIndices.value,attributes:{...a.attributes,getPolygon:a.positions,pickingColors:{size:4,value:o.polygons}},properties:a.properties,numericProps:a.numericProps,featureIds:a.featureIds},n.polygons._normalize=!1,a.triangles&&(n.polygons.data.attributes.indices=a.triangles.value),n.polygonsOutline.data={length:a.primitivePolygonIndices.value.length-1,startIndices:a.primitivePolygonIndices.value,attributes:{...a.attributes,getPath:a.positions,instancePickingColors:{size:4,value:o.polygons}},properties:a.properties,numericProps:a.numericProps,featureIds:a.featureIds},n.polygonsOutline._pathType=`open`,n}var rr=[`points`,`linestrings`,`polygons`],ir={...$(Wn.circle),...$(Wn.icon),...$(Wn.text),...$(Gn),...$(Kn),stroked:!0,filled:!0,extruded:!1,wireframe:!1,_full3d:!1,iconAtlas:{type:`object`,value:null},iconMapping:{type:`object`,value:{}},getIcon:{type:`accessor`,value:e=>e.properties.icon},getText:{type:`accessor`,value:e=>e.properties.text},pointType:`circle`,getRadius:{deprecatedFor:`getPointRadius`}},ar=class extends s{initializeState(){this.state={layerProps:{},features:{},featuresDiff:{}}}updateState({props:e,changeFlags:t}){if(!t.dataChanged)return;let{data:n}=this.props,r=n&&`points`in n&&`polygons`in n&&`lines`in n;this.setState({binary:r}),r?this._updateStateBinary({props:e,changeFlags:t}):this._updateStateJSON({props:e,changeFlags:t})}_updateStateBinary({props:e,changeFlags:t}){let n=nr(e.data,this.encodePickingColor);this.setState({layerProps:n})}_updateStateJSON({props:e,changeFlags:t}){let n=Jn(e.data),r=this.getSubLayerRow.bind(this),i={},a={};if(Array.isArray(t.dataChanged)){let e=this.state.features;for(let t in e)i[t]=e[t].slice(),a[t]=[];for(let o of t.dataChanged){let t=Yn(n,r,o);for(let n in e)a[n].push(Xt({data:i[n],getIndex:e=>e.__source.index,dataRange:o,replace:t[n]}))}}else i=Yn(n,r);let o=tr(i,a);this.setState({features:i,featuresDiff:a,layerProps:o})}getPickingInfo(e){let t=super.getPickingInfo(e),{index:n,sourceLayer:r}=t;return t.featureType=rr.find(e=>r.id.startsWith(`${this.id}-${e}-`)),n>=0&&r.id.startsWith(`${this.id}-points-text`)&&this.state.binary&&(t.index=this.props.data.points.globalFeatureIds.value[n]),t}_updateAutoHighlight(e){let t=`${this.id}-points-`,n=e.featureType===`points`;for(let r of this.getSubLayers())r.id.startsWith(t)===n&&r.updateAutoHighlight(e)}_renderPolygonLayer(){let{extruded:e,wireframe:t}=this.props,{layerProps:n}=this.state,r=`polygons-fill`,i=this.shouldRenderSubLayer(r,n.polygons?.data)&&this.getSubLayerClass(r,Kn.type);if(i){let a=qn(this,Kn.props),o=e&&t;return o||delete a.getLineColor,a.updateTriggers.lineColors=o,new i(a,this.getSubLayerProps({id:r,updateTriggers:a.updateTriggers}),n.polygons)}return null}_renderLineLayers(){let{extruded:e,stroked:t}=this.props,{layerProps:n}=this.state,r=`polygons-stroke`,i=`linestrings`,a=!e&&t&&this.shouldRenderSubLayer(r,n.polygonsOutline?.data)&&this.getSubLayerClass(r,Gn.type),o=this.shouldRenderSubLayer(i,n.lines?.data)&&this.getSubLayerClass(i,Gn.type);if(a||o){let e=qn(this,Gn.props);return[a&&new a(e,this.getSubLayerProps({id:r,updateTriggers:e.updateTriggers}),n.polygonsOutline),o&&new o(e,this.getSubLayerProps({id:i,updateTriggers:e.updateTriggers}),n.lines)]}return null}_renderPointLayers(){let{pointType:e}=this.props,{layerProps:t,binary:n}=this.state,{highlightedObjectIndex:r}=this.props;!n&&Number.isFinite(r)&&(r=t.points.data.findIndex(e=>e.__source.index===r));let i=new Set(e.split(`+`)),a=[];for(let e of i){let i=`points-${e}`,o=Wn[e],s=o&&this.shouldRenderSubLayer(i,t.points?.data)&&this.getSubLayerClass(i,o.type);if(s){let c=qn(this,o.props),l=t.points;if(e===`text`&&n){let{instancePickingColors:e,...t}=l.data.attributes;l={...l,data:{...l.data,attributes:t}}}a.push(new s(c,this.getSubLayerProps({id:i,updateTriggers:c.updateTriggers,highlightedObjectIndex:r}),l))}}return a}renderLayers(){let{extruded:e}=this.props,t=this._renderPolygonLayer(),n=this._renderLineLayers(),r=this._renderPointLayers();return[!e&&t,n,r,e&&t]}getSubLayerAccessor(e){let{binary:t}=this.state;return!t||typeof e!=`function`?super.getSubLayerAccessor(e):(t,n)=>{let{data:r,index:i}=n;return e(en(r,i),n)}}};ar.layerName=`GeoJsonLayer`,ar.defaultProps=ir;export{N as ArcLayer,ce as BitmapLayer,V as ColumnLayer,ar as GeoJsonLayer,vt as GridCellLayer,F as IconLayer,Ae as LineLayer,H as PathLayer,Le as PointCloudLayer,$t as PolygonLayer,He as ScatterplotLayer,Y as SolidPolygonLayer,Un as TextLayer,X as _MultiIconLayer,Rn as _TextBackgroundLayer};