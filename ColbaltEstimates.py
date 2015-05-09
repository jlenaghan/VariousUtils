import sys
import pprint

jitter = (0.12, 0.15, 0.02, -0.05, 0.15, -0.1, -0.15, -0.17)
fats = {
	1:"Auto->Ownership->Entry_Level",
	2:"Auto->Ownership->SUV",
	3:"Auto->Ownership->Entry_Level",
	4:"Auto->Ownership->Luxury",
	5:"Auto->Ownership->Luxury",
	6:"Auto->Ownership->Luxury",
	7:"Auto->Ownership->Entry_Level",
	8:"Auto->Ownership->SUV"
}

fats = {"Auto->Ownership->Entry_Level":(1,6),
 	"Auto->Ownership->SUV":(2,8,7),
 	"Auto->Ownership->Luxury":(3,4,5)
 }

names = ("In Market - Chevy Midsize (Malibu) Likely Owners of Conquests (Ford Fusion, Honda Accord, Toyota Camry, Hyundai Sonata)",
"In Market - Chevy Truck (Silverado) Likely Owners Conquests (Ford F-150, RAM 1500, Toyota Tundra, Nissan Titan)",
"In-Market Buick Midsize Sedan (Verano) Likely Owner Conquests (Lincoln MKZ, Cadillac CTS, Infinit G37, Mercedes C200)",
"In Market Buick SUV/CUV (Enclave) Likely Owner Conquests (BMW X3, Audi Q4, Infiniti JX35, Cadillac SRX)",
"In Market Buick Large Sedan (LaCrosse) Likely Owners (Ford Taurus, Hyundai Eqqus, Audi A8, Chrysler 300)",
"VW Full Size Sedan (Passat) Likely Owner Conquests (Ford Taurus, Chrysler 300, Hyundai Eqqus, Buick Lacrosse)",
"VW Sedan (Jetta) Likely Owner Conquests (Ford Fusion, Honda Accord, Toyota Camry, Nissa Altima, Hundai Sonata)",
"VW Crossover (Tiguan) Likely Owner Conquests (Volvo XC60, Ford Escape, Chevy Equinox, Mazda CX5))"
)

for line in sys.stdin:
	slug, fat, lower, upper = line.strip().split(',')
	fat = fat.replace('"','')
	if fat in fats:
		indices = fats[fat]
		for index in indices:
			jit = float(jitter[index-1])
			value_lower = (1.0/6.0) * 4.0 * float(lower) * (1.0+jit)
			value_upper = (1.0/6.0) * 4.0 * float(upper) * (1.0+jit)
			print slug + ',"' + names[index-1] + '",' + str(int(value_lower)) + ',' + str(int(value_upper))