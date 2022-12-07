db = db.getSiblingDB('masscanresults')

db.createUser({
    user:'admin',
    pwd:'password',
    roles: [
        {
            role: 'readWrite',
            db: 'masscanresults'
    },
    ],
});