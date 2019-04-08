## begin script

MAXNUMBER  = 10
MAXINTENTOS = 20

puts "Bienvenido a ADIVINA TU NUMERO"
puts "Adivina un numero entre 1 y #{MAXNUMBER}"

count = 1
secret_number = rand(MAXNUMBER)+1

print "¿Como te llamas? >"
STDOUT.flush
nombre = gets.chomp
puts "¡ HOLA #{nombre} !"

while true do
  # guess = rand(MAXNUMBER)
  puts " " 
  print "Adivina el numero> "
  STDOUT.flush
  guess = gets.chomp.to_i
  puts "Tu intento es #{guess}"

  if secret_number == guess then
    puts "ADIVINASTE en #{count} intentos!!!"
    puts "FELICITACIONES #{nombre}"
    system("/usr/bin/say --voice=Juan 'felicitaciones #{nombre}'")
    break
  elsif secret_number < guess then
    puts "El numero secreto es MENOR"
  else 
    puts "El numero secreto es MAYOR"
  end
  
  count = count + 1
  
  if count > MAXINTENTOS then
    puts "TE PASASTE DE #{MAXINTENTOS}, PERDISTE!"
    break
  end

end

## end script
