"""
Inicializacao do OpenTelemetry para o analytics-service (traces + metricas).

Este servico e um worker SQS (nao expoe API publica, apenas /health).
Instrumenta Flask (health check e metrica http.server.duration) e botocore
(chamadas SQS e DynamoDB), alem de prover um tracer para spans manuais
no processamento de mensagens.
"""
import os
import logging

from opentelemetry import trace, metrics
from opentelemetry.sdk.resources import Resource, SERVICE_NAME, SERVICE_VERSION, DEPLOYMENT_ENVIRONMENT
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.botocore import BotocoreInstrumentor

log = logging.getLogger(__name__)


def init_telemetry(app):
    """ Inicializa o OpenTelemetry e instrumenta Flask e botocore (SQS/DynamoDB). """
    service_name = os.getenv("OTEL_SERVICE_NAME", "analytics-service")
    environment = os.getenv("DEPLOYMENT_ENVIRONMENT", "dev")
    endpoint = os.getenv(
        "OTEL_EXPORTER_OTLP_ENDPOINT",
        "otel-collector.observability.svc.cluster.local:4317",
    )

    try:
        resource = Resource.create({
            SERVICE_NAME: service_name,
            SERVICE_VERSION: "1.0.0",
            DEPLOYMENT_ENVIRONMENT: environment,
        })

        provider = TracerProvider(resource=resource)
        provider.add_span_processor(BatchSpanProcessor(OTLPSpanExporter(endpoint=endpoint, insecure=True)))
        trace.set_tracer_provider(provider)

        # Metricas: definir o MeterProvider ANTES de instrumentar
        metric_reader = PeriodicExportingMetricReader(
            OTLPMetricExporter(endpoint=endpoint, insecure=True),
            export_interval_millis=15000,
        )
        metrics.set_meter_provider(MeterProvider(resource=resource, metric_readers=[metric_reader]))

        FlaskInstrumentor().instrument_app(app)
        # Instrumenta chamadas boto3/botocore (receive_message, put_item, delete_message)
        BotocoreInstrumentor().instrument()

        log.info(f"[OTel] Telemetria (traces + metricas) inicializada — servico: {service_name}, endpoint: {endpoint}")
    except Exception as e:
        log.warning(f"[OTel] Nao foi possivel inicializar a telemetria: {e}")


def get_tracer():
    """ Retorna um tracer para criar spans manuais no worker. """
    return trace.get_tracer("analytics-service.worker")
