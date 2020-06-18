apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ envs.SERVICE_NAME }}{% if envs.track == "canary" %}-canary{% endif %}
  namespace: {{ envs.KUBE_NAMESPACE }}
  annotations:
    app.gitlab.com/app: {{ envs.CI_PROJECT_PATH_SLUG }}
    app.gitlab.com/env: {{ envs.CI_ENVIRONMENT_SLUG }}
  labels:
    app: {{ envs.SERVICE_NAME }}
    track: {{ envs.track }}
spec:
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 25%
      maxSurge: 1
  replicas: {{ envs.KUBE_REPL | default(value=3) }}
  selector:
    matchLabels:
      app: {{ envs.SERVICE_NAME }}
  template:
    metadata:
      annotations:
        app.gitlab.com/app: {{ envs.CI_PROJECT_PATH_SLUG }}
        app.gitlab.com/env: {{ envs.CI_ENVIRONMENT_SLUG }}
      labels:
        app: {{ envs.SERVICE_NAME }}
        track: {{ envs.track }}
    spec:
      containers:
      - name: {{ envs.SERVICE_NAME }}{% if envs.track == "canary" %}-canary{% endif %}
        image: {{ envs.DOCKER_IMAGE }}
        ports:
          - containerPort: 8788
        env:
{% include "envs.tpli" %}
        resources:
            requests:
                memory: "256Mi"
                cpu: "300m"
            limits:
                memory: "512Mi"
                cpu: "600m"
        livenessProbe:
            httpGet:
                path: /_health
                port: 8788
                httpHeaders:
                - name: Custom-Header
                  value: Awesome
            initialDelaySeconds: 4
            periodSeconds: 1
        readinessProbe:
            httpGet:
                path: /_health
                port: 8788
                httpHeaders:
                - name: Custom-Header
                  value: Awesome
            initialDelaySeconds: 5
            periodSeconds: 1
      imagePullSecrets:
        - name: gitlab-registry
