## ¿Qué es la generación aumentada por recuperación?

La generación aumentada por recuperación (RAG) es el proceso de optimización de la salida de un modelo de lenguaje de gran tamaño, de modo que haga referencia a una base de conocimientos autorizada fuera de los orígenes de datos de entrenamiento antes de generar una respuesta. Los modelos de lenguaje de gran tamaño (LLM) se entrenan con volúmenes de datos amplios y usan miles de millones de parámetros para generar resultados originales en tareas como responder preguntas, traducir idiomas y completar frases. La RAG extiende las ya poderosas capacidades de los LLM a dominios específicos o a la base de conocimientos interna de una organización, todo ello sin la necesidad de volver a entrenar el modelo. Se trata de un método rentable para mejorar los resultados de los LLM de modo que sigan siendo relevantes, precisos y útiles en diversos contextos.

## ¿Por qué es importante la generación aumentada por recuperación?

Los modelos de lenguaje de gran tamaño (LLM) son una tecnología clave de inteligencia artificial (IA) en la que se basan los chatbots inteligentes y otras aplicaciones de procesamiento de lenguaje natural (NLP). El objetivo es crear bots que puedan responder a las preguntas de los usuarios en diversos contextos mediante referencias cruzadas de fuentes de conocimiento autorizadas. Desafortunadamente, la naturaleza de la tecnología del LLM agrega imprevisibilidad en las respuestas del LLM. Además, los datos de entrenamiento del LLM son estáticos y agregan una fecha límite en los conocimientos que tienen.

Los desafíos conocidos de los LLM incluyen los siguientes:

* Presentar información falsa cuando no tiene la respuesta.
* Presentar información desactualizada o genérica cuando el usuario espera una respuesta específica y actual.
* Crear una respuesta de orígenes no autorizados.
* Crear respuestas inexactas debido a una confusión terminológica, en la que diferentes fuentes de entrenamiento utilizan la misma terminología para hablar de cosas diferentes.

Puede pensar en el modelo de lenguaje de gran tamaño como un nuevo empleado demasiado entusiasta que se niega a mantenerse informado de los acontecimientos actuales, pero que siempre responde a todas las preguntas con absoluta confianza. Por desgracia, esta actitud puede afectar de manera negativa a la confianza de los usuarios, lo cual no es algo que quiera que emulen sus chatbots.

La RAG es un enfoque para resolver algunos de estos desafíos. Redirige el LLM para recuperar información relevante de fuentes de conocimiento autorizados y predeterminados. Las organizaciones tienen un mayor control sobre la salida de texto generada y los usuarios obtienen información sobre cómo el LLM genera la respuesta.

## ¿Cuáles son los beneficios de la generación aumentada por recuperación?

### **Implementación rentable**

El desarrollo de chatbots normalmente comienza con un modelo fundacional. Los modelos fundacionales (FM) son LLM accesibles para API entrenados en un amplio espectro de datos generalizados y sin etiquetar. Los costos computacionales y financieros de volver a entrenar a los FM para obtener información específica de la organización o del dominio son altos. La RAG es un enfoque más rentable para introducir nuevos datos en el LLM. Hace que la tecnología de inteligencia artificial generativa (IA generativa) sea más accesible y utilizable.

### **Información actual**

Incluso si los orígenes de datos de entrenamiento originales para un LLM son adecuados para sus necesidades, es difícil mantener la relevancia. La RAG les permite a los desarrolladores proporcionar las últimas investigaciones, estadísticas o noticias a los modelos generativos. Pueden usar la RAG para conectar el LLM de manera directa a redes sociales en vivo, sitios de noticias u otras fuentes de información que se actualizan con frecuencia. El LLM puede entonces proporcionar la información más reciente a los usuarios.

### **Mayor confianza de los usuarios**

La RAG le permite al LLM presentar información precisa con la atribución de la fuente. La salida puede incluir citas o referencias a fuentes. Los usuarios también pueden buscar ellos mismos los documentos de origen si necesitan más aclaraciones o más detalles. Esto puede aumentar la confianza en su solución de IA generativa.

### **Más control para los desarrolladores**

Con la RAG, los desarrolladores pueden probar y mejorar sus aplicaciones de chat de manera más eficiente. Pueden controlar y cambiar las fuentes de información del LLM para adaptarse a los requisitos cambiantes o al uso multifuncional. Los desarrolladores también pueden restringir la recuperación de información confidencial a diferentes niveles de autorización y garantizar que el LLM genere las respuestas adecuadas. Además, también pueden solucionar problemas y hacer correcciones si el LLM hace referencia a fuentes de información incorrectas para preguntas específicas. Las organizaciones pueden implementar la tecnología de IA generativa con mayor confianza para una gama más amplia de aplicaciones.

## ¿Cómo funciona la generación aumentada por recuperación?

Sin la RAG, el LLM toma la información del usuario y crea una respuesta basada en la información en la que se entrenó o en lo que ya sabe. Con la RAG, se ingresa un componente de recuperación de información que utiliza la entrada del usuario para extraer primero la información de un nuevo origen de datos. La consulta del usuario y la información relevante se proporcionan al LLM. El LLM utiliza los nuevos conocimientos y sus datos de entrenamiento para crear mejores respuestas. En las siguientes secciones se ofrece una descripción general del proceso.

### **Crear datos externos**

Los nuevos datos fuera del conjunto de datos del entrenamiento original del LLM se denominan _datos externos_. Pueden provenir de varios orígenes de datos, como API, bases de datos o repositorios de documentos. Los datos pueden existir en varios formatos, como archivos, registros de bases de datos o texto largo. Otra técnica de IA, llamada _incrustación de modelos de lenguaje_, convierte los datos en representaciones numéricas y los almacena en una base de datos vectorial. Este proceso crea una biblioteca de conocimientos que los modelos de IA generativa pueden entender.

### **Recuperar información relevante**

El siguiente paso es realizar una búsqueda de relevancia. La consulta del usuario se convierte en una representación vectorial y se compara con las bases de datos vectoriales. Por ejemplo, piense en un chatbot inteligente que pueda responder a las preguntas de recursos humanos de una organización. Si un empleado busca _“¿Cuántas vacaciones anuales tengo?”_, el sistema recuperará los documentos de la política de vacaciones anuales junto con el historial de vacaciones anteriores del empleado individual. Estos documentos específicos se devolverán porque son muy relevantes para lo que el empleado ha aportado. La relevancia se calculó y estableció mediante cálculos y representaciones vectoriales matemáticas.

### **Aumentar la solicitud de LLM**

A continuación, el modelo RAG aumenta la entrada (o las indicaciones) del usuario al agregar los datos recuperados relevantes en contexto. Este paso utiliza técnicas de ingeniería de peticiones para comunicarse de manera efectiva con el LLM. El indicador aumentado permite que los modelos de lenguajes de gran tamaño generen una respuesta precisa a las consultas de los usuarios.

### **Actualizar datos externos**

La siguiente pregunta podría ser: ¿qué pasa si los datos externos se vuelven obsoletos? A fin de mantener la información actualizada para su recuperación, actualice los documentos de forma asíncrona y actualice la representación incrustada de los documentos. Puede hacerlo mediante procesos automatizados en tiempo real o mediante el procesamiento periódico por lotes. Este es un desafío común en el análisis de datos: se pueden utilizar diferentes enfoques de ciencia de datos para la administración de cambios.

## ¿Cuál es la diferencia entre la generación aumentada por recuperación y la búsqueda semántica?

La búsqueda semántica mejora los resultados de la RAG para las organizaciones que desean agregar amplias fuentes de conocimiento externas a sus aplicaciones de LLM.

## ¿Cómo puede satisfacer AWS sus necesidades de generación aumentada por recuperación?

Amazon Bedrock es un servicio totalmente administrado que ofrece una selección de modelos fundacionales (FM) de alto rendimiento, junto con un amplio conjunto de capacidades, para crear aplicaciones de IA generativa.

Para las organizaciones que administran su propia RAG, Amazon Kendra es un servicio de búsqueda empresarial de alta precisión basado en machine learning.