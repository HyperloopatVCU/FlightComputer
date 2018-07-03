/* LOADOUT */
#define GYRO
#define ACEL
#define HPSN
#define VPSN
#define SERIALMON

#include <MPU9250.h>
#ifndef SERIALMON
#include <Ethernet.h>
#endif
#include<Wire.h>
#include<SPI.h>
#include<Adafruit_VL6180X.h>

#define ID_TAG	1

#define str_l2(X) #X
#define str(X) str_l2(X)

#ifndef SERIALMON
EthernetClient client;
#endif

#if defined(ACEL) || defined(GYRO)
MPU9250 imu(Wire,0x68);
volatile static uint8_t imuerr = 0;
volatile static uint32_t lt = 0;
volatile static uint32_t t = 0;
#endif

#ifdef ACEL
volatile static float agx = 0, agy = 0, agz = 0;
volatile static float aax = 0, aay = 0, aaz = 0;
volatile static float avx = 0;
volatile static float apx = 0;
#endif

#ifdef GYRO
volatile static float ggx = 0, ggy = 0, ggz = 0;
volatile static float gvx = 0, gvy = 0, gvz = 0;
volatile static float gpx = 0, gpy = 0, gpz = 0;
#endif

#ifdef VPSN
Adafruit_VL6180X vps = Adafruit_VL6180X();
volatile static uint8_t vstat = 0;
volatile static float vrange = 0;
#endif

#ifdef HPSN
volatile static float hrange = 0;
const static float hscale = 613.8;
#endif

static void fail(uint8_t s) {
#ifndef SERIALMON
	client.print("{\n\t\"identity\":" str(ID_TAG) "\n\t\"status\":\"Setup failed, code " + String(s, DEC) + "\"\n}");
#endif
	Serial.println("Setup failed, code " + String(s, DEC));
	Serial.flush();
	abort();
}

static void pass() {
#ifndef SERIALMON
	client.print("{\n\t\"identity\":" str(ID_TAG) "\n\t\"status\":\"Setup success\"\n}");
#else
  Serial.println("SUCCESS GENERATED");
#endif
	Serial.flush();
}

void setup() {
	const byte mac[] = {0xde, 0xad, 0xbe, 0xef, 0xfe, ID_TAG};
	const byte gateway[] = {192,168,1,20};
	const byte netmask[] = {255,255,255,0};
	const byte dns[] = {192,168,1,20};
	const byte ip[] = {192,168,1,49};
	const byte server[] = {192,168,1,20};

	Serial.begin(9600);
	while (!Serial);
#ifndef SERIALMON
  Ethernet.begin(mac, ip, dns, gateway, netmask);
  delay(1000);
  Serial.println("Sensor test OK");
	client.setClientTimeout(99000);
	Serial.println(String(client.connect(server, 23), DEC));

	if (client.connected())
		Serial.println("Connected");
	else {
		Serial.println("Could not connect to server");
		fail(1);
	}
#else
  Serial.println("RUNNING IN SERIAL MONITOR MODE, ETHERNET DISABLED.");
#endif

	#if defined(ACEL) || defined(GRYO) || defined(VPSN)
	Wire.begin();
	#endif

	Serial.println("Initializing");
	
#if defined(ACEL) || defined(GYRO)
	if (!imu.begin()) {
		Serial.println("Could not connect to IMU");
		fail(2);
	}
	imu.setAccelRange(MPU9250::ACCEL_RANGE_2G);
	imu.setGyroRange(MPU9250::GYRO_RANGE_250DPS);
	//imu.setDlpfBandwidth(MPU9250::DLPF_BANDWIDTH_20HZ);
	//imu.setSrd(19);
#endif

#if defined(VPSN)
	if (!vps.begin()) {
		Serial.println("Could not connect to VPS");
		fail(3);
	}
	
#endif

#if defined(HPSN) || defined(BRAK)
	analogReference(EXTERNAL);
	delay(200);
#endif
	
	pass();
}

struct {
	const String prelude = "{";
	const String info = "\n\t\"identity\":\"EMS" str(ID_TAG) "\",\n\t\"error\":\"0\"";
#ifdef ACEL
	struct {
		const String prelude = ",\n\t\"accelerometer\":{";
		const String error_prelude = "\n\t\t\"error\":";
		String error = "0";
		struct {
			const String prelude = ",\n\t\t\"acceleration\":{";
			const String info = "\n\t\t\t\"units\":\"g\"";
			const String x_prelude = ",\n\t\t\t\"x\":";
			String x = "0.000000";
			const String y_prelude = ",\n\t\t\t\"y\":";
			String y = "0.000000";
			const String z_prelude = ",\n\t\t\t\"z\":";
			String z = "0.000000";
			const String suff = "\n\t\t}";
		} a;
		struct {
			const String prelude = ",\n\t\t\"velocity\":{";
			const String info = "\n\t\t\t\"units\":\"m/s\"";
			const String x_prelude = ",\n\t\t\t\"x\":";
			String x = "0.000000";
			const String suff = "\n\t\t}";
		} v;
		struct {
			const String prelude = ",\n\t\t\"position\":{";
			const String info = "\n\t\t\t\"units\":\"m\"";
			const String x_prelude = ",\n\t\t\t\"x\":";
			String x = "0.000000";
			const String suff = "\n\t\t}";
		} p;
		const String suff = "\n\t}";
	} accelerometer;
#endif
#ifdef GYRO
	struct{
		const String prelude = ",\n\t\"gyroscope\":{";
		const String error_prelude = "\n\t\t\"error\":";
		String error = "0";
		struct {
			const String prelude = ",\n\t\t\"velocity\":{";
			const String info = "\n\t\t\t\"units\":\"deg/s\"";
			const String x_prelude = ",\n\t\t\t\"x\":";
			String x = "0.000000";
			const String y_prelude = ",\n\t\t\t\"y\":";
			String y = "0.000000";
			const String z_prelude = ",\n\t\t\t\"z\":";
			String z = "0.000000";
			const String suff = "\n\t\t}";
		} v;
		struct {
			const String prelude = ",\n\t\t\"position\":{";
			const String info = "\n\t\t\t\"units\":\"deg\"";
			const String x_prelude = ",\n\t\t\t\"x\":";
			String x = "0.000000";
			const String y_prelude = ",\n\t\t\t\"y\":";
			String y = "0.000000";
			const String z_prelude = ",\n\t\t\t\"z\":";
			String z = "0.000000";
			const String suff = "\n\t\t}";
		} p;
		const String suff = "\n\t}";
	} gyroscope;
#endif
#ifdef VPSN
	struct {
		const String prelude = ",\n\t\"vertical\":{";
		const String error_prelude = "\n\t\t\"error\":";
		String error = "0";
		struct {
			const String prelude = ",\n\t\t\"position\":{";
			const String info = "\n\t\t\t\"units\":\"mm\"";
			const String y_prelude = ",\n\t\t\t\"y\":";
			String y = "0";
			const String suff = "\n\t\t}";
		} p;
		const String suff = "\n\t}";
	} vertical;
#endif
#ifdef HPSN
	struct {
		const String prelude = ",\n\t\"horizontal\":{";
		const String error_prelude = "\n\t\t\"error\":";
		String error = "0";
		struct {
			const String prelude = "\n\t\t\"position\":{";
			const String info = "\n\t\t\t\"units\":\"mm\"";
			const String z_prelude = ",\n\t\t\t\"z\":";
			String z = "0.000000";
			const String suff = "\n\t\t}";
			
		} p;
		const String suff = "\n\t}";
	} horizontal;
#endif
#ifdef BRAK
	struct {
		const String prelude = ",\n\t\"brake\":{"
		const String error_prelude = "\n\t\t\"error\":";
		String error = "0";
		struct {
			const String prelude = "\n\t\t\"position\":{";
			const String info = "\n\t\t\t\"units\":\"mm\"";
			const String dist_prelude = ",\n\t\t\t\"dist\":";
			String dist = "0.000000";
			const String suff = "\n\t\t}";
		}
		const String suff = "\n\t}";
	}
#endif
	const String suff = "\n}\n";
} json;

void send_document() {
	for (uint16_t i = 0; i < (sizeof(json) / sizeof(String)); i++) {
#ifndef SERIALMON
		if (!client.connected()) return;
		client.print( (((String*)(&json))[i]).c_str() );
#else
    Serial.print( (((String*)(&json))[i]).c_str() );
#endif
	}
}

uint8_t c = 0;

void loop() {
#if defined(ACEL) || defined(GYRO)
	t = millis();
	float dt = (t - lt) / 1000;
	lt = t;
	imu.readSensor();
#endif
#ifdef ACEL
	agx -= (aax = imu.getAccelX_mss()) + agx;
	agy -= (aay = imu.getAccelY_mss()) + agy;
	agz -= (aaz = imu.getAccelZ_mss()) + agz;

	avx += aax * dt;

	apx += avx * dt;
#endif
#ifdef GYRO
	ggx -= (gvx = imu.getGyroX_rads()) + ggx;
	ggy -= (gvy = imu.getGyroY_rads()) + ggy;
	ggz -= (gvz = imu.getGyroZ_rads()) + ggz;

	gpx += gvx * dt;
	gpy += gvy * dt;
	gpz += gvz * dt;
#endif

#ifdef VPSN	
	vrange = vps.readRange();
	vstat = vps.readRangeStatus();
	if (vstat == VL6180X_ERROR_NONE) {
		/* TODO: perform redundancy check on accelerometer integration */
	}
#endif

#ifdef HPSN
	hrange = ((1702.268873f / (analogRead(8) + 54.6415201f)) - 0.2798682629f) * 25.4f;
	/*TODO: perform redundancy check on accelerometer integration*/
#endif

#ifndef SERIALMON
  #ifdef COMMAND_CHANNEL
	if (client.available()) {
		char c = client.read();
		Serial.print(c);
	}
  #endif

	if (!client.connected()) {
		Serial.println("Disconnected");
		client.stop();
		fail(-1);
	}
#endif

#ifdef ACEL
	json.accelerometer.a.x = String(aax, 6);
	json.accelerometer.a.y = String(aay, 6);
	json.accelerometer.a.z = String(aaz, 6);

	json.accelerometer.v.x = String(avx, 6);
	
	json.accelerometer.p.x = String(apx, 6);
#endif

#ifdef GYRO
	
	json.gyroscope.v.x = String(gvx, 6);
	json.gyroscope.v.y = String(gvy, 6);
	json.gyroscope.v.z = String(gvz, 6);
	
	json.gyroscope.p.x = String(gpx, 6);
	json.gyroscope.p.y = String(gpy, 6);
	json.gyroscope.p.z = String(gpz, 6);
#endif

#ifdef VPSN
	if (vstat == VL6180X_ERROR_NONE) {
		json.vertical.p.y = String(vrange, 6);
		json.vertical.error = String("\"\"");
	} else if ((vstat >= VL6180X_ERROR_SYSERR_1) && (vstat <= VL6180X_ERROR_SYSERR_5)) {
		json.vertical.error = String("\"SYS_FAIL\"");
	} else if (vstat == VL6180X_ERROR_ECEFAIL)	json.vertical.error = String("\"ECE_FAIL\"");
	else if (vstat == VL6180X_ERROR_NOCONVERGE)	json.vertical.error = String("\"NO_CONVERGE\"");
	else if (vstat == VL6180X_ERROR_RANGEIGNORE)	json.vertical.error = String("\"RANGE_IGNORE\"");
	else if (vstat == VL6180X_ERROR_SNR)		json.vertical.error = String("\"NOISE\"");
	else if (vstat == VL6180X_ERROR_RAWUFLOW)	json.vertical.error = String("\"RAW_UNDER\"");
	else if (vstat == VL6180X_ERROR_RAWOFLOW)	json.vertical.error = String("\"RAW_OVER\"");
	else if (vstat == VL6180X_ERROR_RANGEUFLOW)	json.vertical.error = String("\"RANGE_UNDER\"");
	else if (vstat == VL6180X_ERROR_RANGEOFLOW)	json.vertical.error = String("\"RANGE_OVER\"");
	else						json.vertical.error = String("\"UNKNOWN_ERROR\"");
#endif

#ifdef HPSN
	json.horizontal.p.z = String(hrange, 6);
#endif
	if (!c++) send_document();
}

