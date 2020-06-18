apiVersion: networking.k8s.io/v1beta1
kind: Ingress
metadata:
  name: {{ envs.SERVICE_NAME }}-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /api/$1
spec:
  rules:
  - host: {{ envs.APP_HOST }}
    http:
      paths:
      - path: /api/?(.*)
        backend:
          serviceName: {{ envs.SERVICE_NAME }}-service
          servicePort: 80
---
apiVersion: networking.k8s.io/v1beta1
kind: Ingress
metadata:
  name: {{ envs.SERVICE_NAME }}-ingress-canary
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /api/$1
    nginx.ingress.kubernetes.io/canary: "true"
    nginx.ingress.kubernetes.io/canary-by-header: "X-KALININ"
    nginx.ingress.kubernetes.io/canary-weight: "0"
    nginx.kubernetes.io/canary-by-cookie: "kalinin"
spec:
  rules:
  - host: {{ envs.APP_HOST }}
    http:
      paths:
      - path: /api/?(.*)
        backend:
          serviceName: {{ envs.SERVICE_NAME }}-service-canary
          servicePort: 80
