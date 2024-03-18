#include <iostream>
#include <string>
#include <mqtt/client.h>
#include <mqtt/async_client.h>
#include <json.hpp>

using json = nlohmann::json;

std::map<std::string, float> imu_data;

void on_connect(mqtt::async_client*, mqtt::connect_options&, mqtt::connect_response);
void on_disconnect(mqtt::async_client*, mqtt::disconnect_options&);
void on_message_arrived(mqtt::async_client*, std::string, mqtt::message_ptr);
void process_message(const std::string&);

int main() {
    mqtt::async_client client("tcp://mqtt.eclipseprojects.io:1883", "");
    client.set_callback(on_message_arrived);

    mqtt::connect_options conn_opts;
    client.connect(conn_opts, nullptr, on_connect, on_disconnect);

    while (true) {
        std::this_thread::sleep_for(std::chrono::milliseconds(1000));
    }

    return 0;
}

void on_connect(mqtt::async_client*, mqtt::connect_options&, mqtt::connect_response response) {
    if (!response.is_session_present()) {
        std::cout << "Connection returned result: " << response.get_return_code() << std::endl;
    }

    // Subscribe to the same topic as the IMU
    client.subscribe("ece180da-warmup/venicia/lab4/imu", 1);
}

void on_disconnect(mqtt::async_client*, mqtt::disconnect_options&) {
    std::cout << "Unexpected Disconnect" << std::endl;
}

void on_message_arrived(mqtt::async_client*, std::string, mqtt::message_ptr message) {
    try {
        std::string payload(static_cast<char*>(message->get_payload()), message->get_payload_size());
        process_message(payload);
    } catch (const std::exception& e) {
        std::cerr << "Error processing message: " << e.what() << std::endl;
    }
}

void process_message(const std::string& payload) {
    json data = json::parse(payload);
    imu_data = {
        {"ACC_X", data["ACC_X"].get<float>()},
        {"ACC_Y", data["ACC_Y"].get<float>()},
        {"ACC_Z", data["ACC_Z"].get<float>()},
        {"GYR_X", data["GYR_X"].get<float>()},
        {"GYR_Y", data["GYR_Y"].get<float>()},
        {"GYR_Z", data["GYR_Z"].get<float>()}
    };

    std::cout << "ACC Data: " << imu_data["ACC_X"] << ", " << imu_data["ACC_Y"] << ", " << imu_data["ACC_Z"] << std::endl;
    std::cout << "----------------------------" << std::endl;
    std::cout << "GYR Data: " << imu_data["GYR_X"] << ", " << imu_data["GYR_Y"] << ", " << imu_data["GYR_Z"] << std::endl;
    std::cout << "----------------------------" << std::endl;
    std::cout << "Direction:   X       Y       Z" << std::endl;
}
