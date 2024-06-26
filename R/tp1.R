## -------------------------------------------------------------------------------------------------------------------------
## Generación de muestras X e Y
set.seed(123) 
# Definir parámetros
n <- 200 # cant observ
μX <- 10 # media de x
σX <- 2 # desv std x
μY <- 15 # media de y
σY <- 3 # desv std y

# Generar random variables dependientes
Z1 <- rnorm(n)
Z2 <- rnorm(n)

x <- μX + σX * Z1
y <- μY + σY * Z2

dat <- cbind(x,y) #junto los valores en una lista



## -------------------------------------------------------------------------------------------------------------------------
# library(ggplot2)
# pairs(dat) # otra forma de verificar relación, una matriz de diagramas de dispersión
plot(dat)


## -------------------------------------------------------------------------------------------------------------------------
# Realizo regresión lineal 
regresion <- lm(y ~ x, data = data.frame(dat))
summary(regresion)
#boxplot(regresion$residuals)


## -------------------------------------------------------------------------------------------------------------------------
# library(psych)
# library(GGally)
#ggpairs(dat, aes(alpha = 0.5),lower = list(continuous = "smooth"))

# Creamos el gráfico
plot(x, y)
# Línea de regresión
abline(lm(y ~ x))


## -------------------------------------------------------------------------------------------------------------------------
set.seed(123)  # Set a seed for reproducibility

# Definir parámetros
n <- 200 # cant observ
μX <- 10
σX <- 2
μY <- 15
σY <- 3
ρ <- 0.7 #grado de correlación

# Generar random variables dependientes
Z1 <- rnorm(n)
Z2 <- rnorm(n)

x <- μX + σX * Z1
y <- μY + σY * (ρ * x + sqrt(1 - ρ^2) * Z2)
dat <- cbind(x,y) #junto los valores en una lista
plot(dat)
abline(lm(y ~ x))


## -------------------------------------------------------------------------------------------------------------------------
# ggpairs(dat, aes(alpha = 0.5),lower = list(continuous = "smooth"))


## -------------------------------------------------------------------------------------------------------------------------
# Realizo regresión lineal 
modelo <- lm(y ~ x, data = data.frame(dat))
summary(modelo)


## -------------------------------------------------------------------------------------------------------------------------
set.seed(123)
Z1 <- rnorm(20)
x <- μX + σX * Z1
predict(object=modelo, newdata=data.frame(x))


## -------------------------------------------------------------------------------------------------------------------------
set.seed(123)
# Establecer numero de simulaciones
num_simulations <- 1000
n <- 100
# Establecer parametros del modelo
intercept <- 4.9
beta <- 1.02
error_std_dev <- 2.138

# Inicializar vectores que contendrán los coeficientes estimados
pendientes <- vector(length = num_simulations)
intercepts <- vector(length = num_simulations)

# Perform the simulations
for (i in 1:num_simulations) {
  # Generate the independent variable (x)
  Z1 <- rnorm(n)
  x <- μX + σX * Z1
  
  # Generate the dependent variable (y) using the model equation
  y <- intercept + beta * x + rnorm(n, 0, error_std_dev)
  #μY + σY * (ρ * Z1 + sqrt(1 - ρ^2) * Z2)
  
  # Fit the linear regression model
  model <- lm(y ~ x)
  pendientes[i] <- model$coefficients[2]
  intercepts[i] <- model$coefficients[1]
}




## -------------------------------------------------------------------------------------------------------------------------
par(mfrow = c(1, 2))
hist(pendientes, main = "Distribución de Pendiente",xlab = "Pendiente")
abline(v = mean(pendientes), col="red", lwd=3, lty=2)
hist(intercepts, main = "Distribución de Intercept", xlab = "Intercept")
abline(v = mean(intercepts), col="red", lwd=3, lty=2)



## -------------------------------------------------------------------------------------------------------------------------
par(mfrow = c(1, 2))
plot(density(pendientes, width = .2))
plot(density(intercepts, width = .2))


## -------------------------------------------------------------------------------------------------------------------------
# Establecer numero de simulaciones
set.seed(123)
num_simulations <- 1000
n <- 100
# Establecer parametros del modelo
intercept <- 4.9
beta <- 2
error_std_dev <- 1

# Inicializar vectores que contendrán los coeficientes estimados
pendientes <- vector(length = num_simulations)
intercepts <- vector(length = num_simulations)

# Perform the simulations
for (i in 1:num_simulations) {
  # Generate the independent variable (x)
  x <- runif(n)
  # plot(x)
  
  # Generate the dependent variable (y) using the model equation
  y <- intercept + beta * x + rnorm(n, 0, error_std_dev)
  
  # Fit the linear regression model
  model <- lm(y ~ x)
  pendientes[i] <- model$coefficients[2]
  intercepts[i] <- model$coefficients[1]
}

par(mfrow = c(2, 2))
hist(pendientes, main = "Distribución de Pendiente Estimadas",xlab = "Pendiente")
abline(v = mean(pendientes), col="red", lwd=3, lty=2)
hist(intercepts, main = "Distribución de Intercept Estimados", xlab = "Intercept")
abline(v = mean(intercepts), col="red", lwd=3, lty=2)
plot(density(pendientes, width = .2))
plot(density(intercepts, width = .2))

