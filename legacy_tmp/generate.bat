@echo off
echo Removing existing clients...
if exist nifi-client rmdir /s /q nifi-client
if exist registry-client rmdir /s /q registry-client

echo Generating NiFi client...
java -jar swagger-codegen-cli-3.0.68.jar generate ^
-i ../resources/client_gen/api_defs/nifi-2.3.0.json ^
-l python ^
-c nifi.conf.json ^
-t swagger_templates_v3 ^
-o nifi-client

echo.
echo Generating Registry client...
java -jar swagger-codegen-cli-3.0.68.jar generate ^
-i ../resources/client_gen/api_defs/registry-2.3.0.json ^
-l python ^
-c registry.conf.json ^
-t swagger_templates_v3 ^
-o registry-client 