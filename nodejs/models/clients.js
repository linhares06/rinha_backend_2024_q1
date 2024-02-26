const mongoose = require('../database/mongoose.service').mongoose;
const Schema = mongoose.Schema;

const clientsSchema = new Schema({
    id: { type: Number, integer: true },
    limite: { type: Number, integer: true },
    saldo: { type: Number, integer: true },
    transactions: Array,
});

const Clients = mongoose.model('Clients', clientsSchema);

exports.getClientById = async (id) => {
    return await Clients.findOne({ id: id }, {_id: false, transactions: false});
};

exports.getClientLastTenTransactions = async (clientId) => {
    const id = parseInt(clientId);
    const pipeline = [
        {'$match': {id: id}},
        {'$project': {'_id': false, 'id': false, 'limite': false, 'saldo': false}},
        {'$unwind': '$transactions'},
        {'$sort': {'transactions.realizada_em': -1}},
        {'$limit': 10}
    ];
    return await Clients.aggregate(pipeline);
}

exports.saveClientTransaction = async (client, transactionDict) => {
    try {
        const result = await Clients.updateOne(
            { id: client.id },
            { $set: { saldo: client.saldo }, $push: { transactions: transactionDict } },
            { upsert: true }
        );
        if (result.modifiedCount === 0) {
            throw new Error('Falha ao inserir dados.')
        }
    } catch (error) {
        throw new Error(`Failed to save transaction: ${error.message}`);
    }
}

exports.list = async () => {
    return await Clients.find({}, {_id: false, transactions: false});
};