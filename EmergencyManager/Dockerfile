# syntax=docker/dockerfile:1

FROM maven:3.8.3-openjdk-17-slim AS builder

WORKDIR /app

COPY pom.xml ./
COPY src ./src

RUN mvn clean install package -DskipTests

FROM eclipse-temurin:17-jdk-jammy

WORKDIR /app

COPY --from=builder /app/target/EmergencyManager-*-shaded.jar ./app.jar
COPY --from=builder /app/src/main/resources/config.properties ./config.properties

CMD ["java", "-jar", "app.jar"]
