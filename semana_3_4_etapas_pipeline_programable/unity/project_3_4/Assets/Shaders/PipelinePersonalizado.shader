Shader "Custom/PipelinePersonalizado"
{
    Properties
    {
        _MainTex ("Texture", 2D) = "white" {}
        _Color ("Base Color", Color) = (0.2, 0.6, 1.0, 1.0)
        _FresnelPower ("Fresnel Power", Range(0.1, 10.0)) = 2.0
        _CustomTime ("Custom Time", Float) = 0.0
    }
    SubShader
    {
        Tags { "RenderType"="Opaque" "Queue"="Geometry" }
        LOD 100

        Pass
        {
            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag
            
            #include "UnityCG.cginc"

            struct appdata
            {
                float4 vertex : POSITION;
                float3 normal : NORMAL;
                float2 uv : TEXCOORD0;
            };

            struct v2f
            {
                float2 uv : TEXCOORD0;
                float3 normalWS : NORMAL;
                float3 viewDirWS : TEXCOORD1;
                float4 vertex : SV_POSITION;
            };

            sampler2D _MainTex;
            float4 _MainTex_ST;
            float4 _Color;
            float _FresnelPower;
            float _CustomTime;

            v2f vert (appdata v)
            {
                v2f o;
                
                // --- 1. VERTEX SHADER - TRANSFORMACIONES Y DEFORMACIONES ---
                // Deformar los vértices basado en onda senoidal sobre el tiempo
                float waveX = sin(v.vertex.x * 5.0 + _CustomTime * 3.0) * 0.12;
                float waveY = sin(v.vertex.y * 4.0 + _CustomTime * 2.1) * 0.08;
                v.vertex.z += waveX + waveY;
                
                // Mapeo Model Space -> World -> View -> Clip Space
                o.vertex = UnityObjectToClipPos(v.vertex);
                o.uv = TRANSFORM_TEX(v.uv, _MainTex);
                
                // Calcular normales al World Space y la dirección de la cámara (ViewDir) para Fresnel
                o.normalWS = UnityObjectToWorldNormal(v.normal);
                float3 worldPos = mul(unity_ObjectToWorld, v.vertex).xyz;
                o.viewDirWS = normalize(_WorldSpaceCameraPos - worldPos);
                
                return o;
            }

            fixed4 frag (v2f i) : SV_Target
            {
                // --- 2. FRAGMENT SHADER - CALCULO DE COLOR, ILUMINACIÓN ---
                // Re-normalizar las variables interpoladas (varyings)
                float3 n = normalize(i.normalWS);
                
                // Iluminación direccional simulada (Lambertiana pura)
                float3 lightDir = normalize(float3(0.5, 1.0, 0.5));
                float diff = max(0.0, dot(n, lightDir));
                
                // Mezcla Base
                fixed4 baseCol = tex2D(_MainTex, i.uv) * _Color;
                fixed3 litColor = baseCol.rgb * (0.15 + 0.85 * diff);
                
                // --- ETAPA AVANZADA: EFECTO FRESNEL ---
                float fresnel = pow(1.0 - max(dot(n, i.viewDirWS), 0.0), _FresnelPower);
                fixed3 rimColor = fixed3(0.2, 0.6, 1.0) * fresnel;
                
                return fixed4(litColor + rimColor, 1.0);
            }
            ENDCG
        }
    }
}
