# The clinic kiosks show the same site from a small container (tagged with the commit it was built from).
FROM public.ecr.aws/docker/library/python:3.12-slim
COPY dist/ /srv/
USER 10001
EXPOSE 8080
CMD ["python", "-m", "http.server", "8080", "--directory", "/srv"]
