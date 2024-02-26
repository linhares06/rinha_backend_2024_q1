const { body, validationResult } = require('express-validator');

const Client = require('../models/clients');


exports.routesConfig = function (app) {

    app.post('/clientes/:id/transacoes', [
        body('valor').isInt({ min: 1 }).withMessage("Valor deve ser um inteiro positivo."),
        body('tipo').isIn(['c', 'd']).withMessage("Deve ser 'c' para cedito ou 'd' para debito."),
        body('descricao').isLength({ min: 1, max: 10 }).withMessage("Descricao deve conter entre 1 e 10 caracteres."),
    ], async (req, res) => {
        const errors = validationResult(req);
        if (!errors.isEmpty()) {
            return res.status(400).json({ errors: errors.array() });
        }

        const clientId = req.params.id;
        const client = await Client.getClientById(clientId);
        if (!client) {
            return res.status(404).json({ error: "Id inexistente." });
        }

        const valor = req.body.valor;
        const tipo = req.body.tipo;
        const descricao = req.body.descricao;
        let saldo;

        if (tipo === 'd') {
            saldo = client.saldo - valor;
            if (saldo + client.limite < 0) {
                return res.status(422).json({'limite': 'Ta querendo gastar mais do que tem, champz'});
            }
        } else {
            saldo = client.saldo + valor;
        }
        
        client.saldo = saldo;

        const time_now = new Date();
        time_now.setHours(time_now.getHours() - 3);

        const transactionDict = {
            valor: valor,
            tipo: tipo,
            descricao: descricao,
            realizada_em: time_now
        };

        Client.saveClientTransaction(client, transactionDict).then(() => {
            res.json({limite: client.limite, saldo: client.saldo});
        })
        .catch((error) => {
            res.status(500).json({ error: error.message });
        });
    });

    app.get('/clientes/:id/extrato', async (req, res) => {
        const clientId = req.params.id;

        try {
            const client = await Client.getClientById(clientId);
            if (!client) {
                return res.status(404).json({ error: "Id inexistente." });
            }

            const transactions = await Client.getClientLastTenTransactions(clientId);
            
            const time_now = new Date();
            time_now.setHours(time_now.getHours() - 3);

            const statements = {
                saldo: {
                        total: client.saldo,
                        data_extrato: time_now,
                        limite: client.limite
                    },
                    ultimas_transacoes: transactions.map(transaction => ({
                        valor: transaction.transactions.valor,
                        tipo: transaction.transactions.tipo,
                        descricao: transaction.transactions.descricao,
                        realizada_em: transaction.transactions.realizada_em,
                    })),
            };
            res.json(statements);
        } catch (error) {
            console.error(error);
            return res.status(422).json({ error: "Can't process." });
        }

    });

    app.get('/clientes', (req, res) => {
        Client.list().then((result) => {
            res.status(200).send(result);
        })
    });
}
