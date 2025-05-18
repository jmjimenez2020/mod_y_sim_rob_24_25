# mod_y_sim_rob_24_25

En este repositorio se tienen los archivos necesarios para la ejecucion del mundo en gazebo con el robot creado en la practica 2, con la posibilidad de teleoperar el robot y usar el brazo para coger cubos y situarlos en el compartimento del mismo. 

Explicaremos como poner en ejecucion la practica, con los comandos necesarios, donde descargar el rosbag, con los datos de los topics de la imu y los joints del robot, y analizaremos las graficas del gasto, posicion de las ruedas y aceleracion con respecto al tiempo, describiendo el comportamiento del robot en momentos especificos de la teleoperacion. 

Antes de eso, para la parte a de la practica se pedia lanzar el robot_state_publisher y visualizar el robot en Rviz, y con la interfaz de usuario poder mover los joints, esto se puede apreciar en la siguiente imagen.

![Robot en Rviz](./media/imagen_parte_a.png)

Ademas, tambien se pedia una imagen para poder visualizar el arbol de transformadas entre los links del robot
[PDF transformadas](./media/arbol_transformadas.pdf)

---

## Analisis de las graficas

### 1. G Parcial - Tiempo


![G Parcial - Tiempo](./media/tiempo_vs_g_parcial.png)

### 2. Posicion Ruedas - Tiempo


![Posicion Ruedas - Tiempo](./media/tiempo_vs_pos_ruedas.png)

### 3. Aceleracion - Tiempo


![Aceleracion - Tiempo](./media/tiempo_vs_aceleracion.png)

---

## Rosbag

El rosbag generado mientras el robot se desplaza hacia la caja situada en (5,0), posteriormente coge la caja, la situa en su compartimento y vuelve a la posicion inicial se guarda en el rosbag que esta enlazado a continuacion. En el, unicamente se estaran registrando los topics /imu/data y /joint_states. El archivo se encuentra tambien en el repo en la carpeta rosbag.

[Descargar Rosbag](https://github.com/jmjimenez2020/mod_y_sim_rob_24_25/tree/main/rosbag)

He añadido tambien un fichero con codigo que permite crear las graficas que se pedian en la practica con los datos del rosbag.

---

## Ejecucion

Para poder ejecutar la practica en tu propio ordenador vamos a ir siguiendo una serie de pasos:
- Clonar el repositorio en tu ordenador
  
  ```git clone https://github.com/jmjimenez2020/mod_y_sim_rob_24_25.git```
- Compilar el repo y comprobar que se haya hecho correctamente
  ```
  colcon build
  source install/setup.bash
- Ejecutar los launchers. Primero iremos con el mundo de gazebo, en el que cargamos el robot tambien
  
  ```ros2 launch urjc_excavation_world urjc_excavation_msr.launch.py```
- Ejecutar el move_group
  
  ```ros2 launch rover_moveit_config move_group.launch.py```
- Ejecutar el launcher de los controladores
  
  ```ros2 launch robot_model_description robot_controllers.launch.py```
- Ejecutar la teleoperacion
  
  ```ros2 run teleop_twist_keyboard teleop_twist_keyboard```

Antes de ejecutar todo esto tendremos que tener instalados una serie de paquetes, de lo contrario tendremos fallos que nos impediran ejecutar los comandos. Podemos instalarlos mediante:

```sudo apt install ros-jazzy-<nombre del paquete>```

Si hemos hecho todo lo anterior y no hemos tenido ningun fallo, entonces podremos pasar a mover el robot por el mundo con la teleoperacion. Cuando lanzamos el mundo de gazebo tambien se abre en otra pestaña Rviz, cosa que permite que en cualquier momento podamos planificar que el brazo se desplace de una posicion a otra o que el gripper se abra o se cierre

![Robot en gazebo](./media/imagen_simulacion.png)
