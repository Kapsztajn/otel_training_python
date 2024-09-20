-- Test Data
INSERT INTO users (user_id, email, first_name, last_name)
VALUES
('6321d983-896e-41b9-b220-f218ee40190d', 'john.doe@example.com', 'John', 'Doe'),
('501a67c6-49fe-4fee-bb4b-0350a36b18c0', 'jane.smith@example.com', 'Jane', 'Smith'),
('cc95aa06-53fe-4b37-baff-af65ede3ec2a', 'alice.jones@example.com', 'Alice', 'Jones'),
('bbc512e7-a160-440d-add0-4e05fe02d0e1', 'bob.brown@example.com', 'Bob', 'Brown'),
('b127dbbb-652c-4e78-82ca-d420174e8428', 'charlie.green@example.com', 'Charlie', 'Green'),
('dce80da6-e4c3-4471-a1b5-08b84a3902f6', 'diana.white@example.com', 'Diana', 'White'),
('18979516-287d-4dfd-977b-92803ea51f7e', 'elizabeth.black@example.com', 'Elizabeth', 'Black'),
('7e65a387-199e-4bb3-b6c9-5131021708bb', 'frank.martin@example.com', 'Frank', 'Martin'),
('c82ef982-df91-4456-91b8-c664dc3517eb', 'george.king@example.com', 'George', 'King'),
('f1853f68-7d3f-4452-becf-c30f871bb98d', 'harry.potter@example.com', 'Harry', 'Potter');

-- Test Data
INSERT INTO rooms (room_id, room_no, floor, price, building)
VALUES
('626c273c-6783-4bf8-92ef-8fbd253d8801', 'R101', 1, 120.50, 'Building A'),
('054cba16-fdf4-4746-b644-3e091b4cc8c7', 'R102', 1, 130.00, 'Building A'),
('40a24155-8625-4b27-886f-170f3e06e923', 'R201', 2, 150.75, 'Building A'),
('765c546c-912f-4a20-9434-f7381825b287', 'R202', 2, 160.00, 'Building A'),
('cb8bf7f9-8108-4514-bf03-e526c98b190f', 'R301', 3, 180.00, 'Building B'),
('46c04767-c059-42cc-86b8-ee2b0b8a955b', 'R302', 3, 190.50, 'Building B'),
('843be14d-f6bf-48bc-8bd4-4739b14425b5', 'R401', 4, 200.00, 'Building B'),
('05c9183c-d211-4c3b-ae8d-f295ad242138', 'R402', 4, 210.25, 'Building C'),
('cc719998-09bd-4ec5-a21d-0c758abefa6e', 'R501', 5, 220.75, 'Building C'),
('ceb5fe4b-e6a1-4e44-948b-494eb53829f3', 'R502', 5, 230.00, 'Building C');

-- Test Data
INSERT INTO reservations (reservation_id, user_id, room_id)
VALUES
('7793d466-b64c-4a70-ad7a-d481c7dc2ccd', '6321d983-896e-41b9-b220-f218ee40190d', '626c273c-6783-4bf8-92ef-8fbd253d8801'),
('b0fc7698-6dd4-4dff-babb-3d6dd4f70861', '501a67c6-49fe-4fee-bb4b-0350a36b18c0', '054cba16-fdf4-4746-b644-3e091b4cc8c7'),
('915f4cd9-a0d8-41be-8310-1748039e8f78', 'cc95aa06-53fe-4b37-baff-af65ede3ec2a', '40a24155-8625-4b27-886f-170f3e06e923'),
('dfac72c9-3251-43fc-ab7f-38f1028c40b5', 'bbc512e7-a160-440d-add0-4e05fe02d0e1', '765c546c-912f-4a20-9434-f7381825b287'),
('ec109c20-c405-41a2-b5d5-668662df63e9', 'b127dbbb-652c-4e78-82ca-d420174e8428', 'cb8bf7f9-8108-4514-bf03-e526c98b190f');
