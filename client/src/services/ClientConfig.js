const Config = {
    FRONTEND_VERSION: "1.2.5",
    SERVER_VERSION_COMPATABILITY: ["1.2.2"],
    VERSION_CHECK_ENABLED: true,
    TEST_BUILD: false,

    WEBSOCKET_URL: "ws://localhost:8765",
    SOCKET_RETRY_THRESHOLD: 5,

    WEIGHT_INTERVALS: 10,
    SKIN_CHANGER_WARNING_THRESHOLD: 6,

    NAVIGATION_ENABLED: true,
    ENABLED_PAGES: {
        "collection": true,
        "loadouts": false,
        "buddies": true,
    }
}

var ServerVersion = "";

function setVersion(version) {
    ServerVersion = version;
}

const loadoutGridOrder = [
    [
        {
            "type": "weapon",
            "sidearm": true,
            "uuid": "29a0cfab-485b-f5d5-779a-b59f85e204a8",
            "displayName": "Classic",
        },
        {
            "type": "weapon",
            "sidearm": false,
            "uuid": "f7e1b454-4ad4-1063-ec0a-159e56b58941",
            "displayName": "Stinger",
        },
        {
            "type": "weapon",
            "sidearm": false,
            "uuid": "ae3de142-4d85-2547-dd26-4e90bed35cf7",
            "displayName": "Bulldog",
        },
        {
            "type": "weapon",
            "sidearm": false,
            "uuid": "c4883e50-4494-202c-3ec3-6b8a9284f00b",
            "displayName": "Marshal",
        },
    ],
    [
        {
            "type": "weapon",
            "sidearm": true,
            "uuid": "42da8ccc-40d5-affc-beec-15aa47b42eda",
            "displayName": "Shorty",
        },
        {
            "type": "weapon",
            "sidearm": false,
            "uuid": "462080d1-4035-2937-7c09-27aa2a5c27a7",
            "displayName": "Spectre",
        },
        {
            "type": "weapon",
            "sidearm": false,
            "uuid": "4ade7faa-4cf1-8376-95ef-39884480959b",
            "displayName": "Guardian",
        },
        {
            "type": "weapon",
            "sidearm": false,
            "uuid": "a03b24d3-4319-996d-0f8c-94bbfba1dfc7",
            "displayName": "Operator",
        },
    ],
    [
        {
            "type": "weapon",
            "sidearm": true,
            "uuid": "44d4e95c-4157-0037-81b2-17841bf2e8e3",
            "displayName": "Frenzy",
        },
        {
            "type": "weapon",
            "sidearm": false,
            "uuid": "910be174-449b-c412-ab22-d0873436b21b",
            "displayName": "Bucky",
        },
        {
            "type": "weapon",
            "sidearm": false,
            "uuid": "ee8e8d15-496b-07ac-e5f6-8fae5d4c7b1a",
            "displayName": "Phantom",
        },
        {
            "type": "weapon",
            "sidearm": false,
            "uuid": "55d8a0f4-4274-ca67-fe2c-06ab45efdf58",
            "displayName": "Ares",
        },
    ],
    [
        {
            "type": "weapon",
            "sidearm": true,
            "uuid": "1baa85b4-4c70-1284-64bb-6481dfc3bb4e",
            "displayName": "Ghost",
        },
        {
            "type": "weapon",
            "sidearm": false,
            "uuid": "ec845bf4-4f79-ddda-a3da-0db3774b2794",
            "displayName": "Judge",
        },
        {
            "type": "weapon",
            "sidearm": false,
            "uuid": "9c82e19d-4575-0200-1a81-3eacf00cf872",
            "displayName": "Vandal",
        },
        {
            "type": "weapon",
            "sidearm": false,
            "uuid": "63e6c2b6-4a8e-869c-3d4c-e38355226584",
            "displayName": "Odin",
        },
    ],
    [
        {
            "type": "weapon",
            "sidearm": true,
            "uuid": "e336c6b8-418d-9340-d77f-7a9e4cfe0702",
            "displayName": "Sheriff",
        },
        {
            "type": "weapon",
            "sidearm": false,
            "uuid": "5f0aaf7a-4289-3998-d5ff-eb9a5cf7ef5c",
            "displayName": "Outlaw"
        },
        {
            "type": "placeholder",
        },
        {
            "type": "weapon",
            "sidearm": false,
            "uuid": "2f59173c-4bed-b6c3-2191-dea9b58be9c7",
            "displayName": "Melee",
        },
    ],
]

export {Config, ServerVersion, setVersion, loadoutGridOrder}
