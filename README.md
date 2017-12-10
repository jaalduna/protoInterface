# protoInterface
Módulo para conversar con dispositivos electrónicos directamente desde Python

## Diseño de clases
ProtoInterface esta basado en el integrado FT2232H. Las configuraciones se realizan a través de este integrado. 
En Python ya existe una librería o módulo denominado "Device", dentro del paquete pylibftdi.

### Clase protoInterface
Tiene sentido entonces crear la clase ProtoInterface heredada a partir de Device. de esta forma se hereda la capacidad de hablar al dispositivo y se puede
definir adicionalmente los parametros y métodos para ProtoInterface.

### Clase gpio



