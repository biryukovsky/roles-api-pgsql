apiVersion: v1
kind: Service
metadata:
  name: {{ envs.SERVICE_NAME }}-service
spec:
  selector:
    app: {{ envs.SERVICE_NAME }}
    track: stable
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8788

---
apiVersion: v1
kind: Service
metadata:
  name: {{ envs.SERVICE_NAME }}-service-canary
spec:
  selector:
    app: {{ envs.SERVICE_NAME }}
    track: canary
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8788
